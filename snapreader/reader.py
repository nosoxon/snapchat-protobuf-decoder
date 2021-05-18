import sqlite3

from time import ctime

from .contacts import contacts
from .content_pb2 import root as content_root

def parse_timestamp_ms(x):
	return ctime(x / 1000.0)

def parse_raw_uuid(x):
	h = x.hex()
	return '{}-{}-{}-{}-{}'.format(h[:8], h[8:12], h[12:16], h[16:20], h[20:])

class Message:
	def __init__(self, sender, message, timestamp):
		self.sender = sender
		self.message = message
		self.timestamp = timestamp

def parse_blob(blob):
	root = content_root()
	root.ParseFromString(blob)

	sender = parse_raw_uuid(root.sender.id)
	timestamp = parse_timestamp_ms(root.impression.created_at)

	if root.contents.type != root.contents.MESSAGE:
		return None

	message = root.contents.payload.message.text

	return Message(sender, message, timestamp)


q = (
	'select message_content from conversation_message ' +
	'where client_conversation_id="{}" ' +
	'order by creation_timestamp asc'
)

def read_db(path, client_conversation_id):
	with sqlite3.connect(path) as conn:
		conn.row_factory = sqlite3.Row

		cursor = conn.cursor()
		cursor.execute(q.format(client_conversation_id))

		messages = [ parse_blob(row[0]) for row in cursor.fetchall() ]

	return [ m for m in messages if m is not None ]
