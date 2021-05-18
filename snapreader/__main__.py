#!/usr/bin/python3
import json
import sys

from .reader import read_db

filename = sys.argv[1]
contacts_path = sys.argv[2]
client_conversation_id = sys.argv[3]

with open(contacts_path) as f:
	contacts = json.loads(f.read())

messages = read_db(filename, client_conversation_id)

last_sender = None
for m in messages:
	prefix = ''
	if m.sender != last_sender:
		prefix = '{}>'.format(contacts[m.sender]['username'])
	last_sender = m.sender

	print(f'{prefix:>20}  {m.message:140}{m.timestamp}')
