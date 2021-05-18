import json
from time import ctime

types = {
  "root": {
    1: ("int32",          "server_message_id"),
    2: ("Sender",         "sender"),
    3: ("Conversation",   "conversation"),
    4: ("Contents",       "contents"),
    6: ("ImpressionMeta", "impression"),
    7: ("int64",          "client_resolution_id"),
    9: ("ServerMetadata", "server_meta"),
  },

  "Sender": {
    1: ("friend_id", "id"),
  },

  "Conversation": {
    1: ("ConversationMeta", "meta"),
  },
  "ConversationMeta": {
    1: ("ConversationID", "id"),
    2: ("int64", "version"),
  },
  "ConversationID": {
    # client_conversation_id
    1: ("raw_uuid", "id"),
  },

  "ImpressionMeta": {
    1:  ("timestamp_ms", "created_at"),
    2:  ("timestamp_ms", "read_at"),
    4:  ("UserID",       "read_by"),
    6:  ("UserID",       "saved_by"),
    11: ("int64",        "version_id"),
  },
  "UserID": {
    1:  ("friend_id", "id"),
  },

  "ServerMetadata": {
    1: ("ServerMessage", "msg"),
  },

  "ServerMessage": {
    # 8B = server_message_id, 8B = lower half conversation_id
    1: ("raw_uuid", "id"),
  },

  "Contents": {
    2: ("enum content_type", "type"),
    4: ("Payload",           "payload"),
    5: ("ContentMeta",       "meta"),
  },

  "enum content_type": {
    1: "MESSAGE",
    2: "VIDEO",
    3: "SNAP_CONTACT",
  },

  "Payload": {
    2:  ("MessagePayload",     "message"),
    5:  ("SnapContactPayload", "snap_contact"),
    11: ("SnapPayload",        "snap"),
  },
  "MessagePayload": {
    1: ("string", "text"),
  },
  "SnapContactPayload": {
    7: ("SCP_L2", "s"),
  },
  "SCP_L2": {
    1: ("SCP_L3", "s"),
  },
  "SCP_L3": {
    1: ("raw_uuid", "contact_id"),
  },


  "ContentMeta": {
    1: ("ContentMetaPayload", "payload"),
  },
  "ContentMetaPayload": {
    3: ("ContentObject", "obj"),
    8: ("varint",        "x"),
  },
  "ContentObject": {
    2: ("ContentObjectMeta", "meta"),
  },
  "ContentObjectMeta": {
    2:  ("string",     "id"),
    4:  ("TimestampS", "ts"),
    9:  ("varint",     "x"),
    10: ("varint",     "y"),
    12: ("varint",     "z"),
  },

  "TimestampS": {
    1: ("timestamp_s", "value"),
  },

  "SnapPayload": {
    5:  ("Snap", "snap"),
    #13: (),
    #14: (),
  },

  "Snap": {
    1: ("SnapPacket", "packet"),
    #2: (),
  },

  "SnapPacket": {
    1: ("PhotoPacket", "photo"),
    2: ("TextPacket",  "text"),
  },

  "PhotoPacket": {
    2:  ("varint",          "x"),
    4:  ("KeyIV64",         "key_iv_base64"),
    5:  ("PhotoResolution", "resolution"),
    12: ("varint",          "y"),
    19: ("KeyIVRaw",        "key_iv_raw"),
  },

  "TextPacket": {
    1: ("string", "content"),
  },

  "KeyIV64": {
    1: ("string", "key"),
    2: ("string", "iv"),
  },

  "PhotoResolution": {
    1: ("int32", "width"),
    2: ("int32", "height"),
  },

  "KeyIVRaw": {
    1: ("bytestring", "key"),
    2: ("bytestring", "iv"),
  },
}

with open("contacts.json") as f:
  contacts = json.loads(f.read())

def parse_friend_id(x, type):
  id = parse_raw_uuid(x, type)
  return contacts[id] + f' [{id}]'

def parse_bytestring(x, type):
  return x.read().hex().lower()

def parse_timestamp_s(x, type):
  return ctime(x)

def parse_timestamp_ms(x, type):
  return ctime(x / 1000.0)

def parse_raw_uuid(x, type):
  h = x.read().hex()
  return '{}-{}-{}-{}-{}'.format(h[:8], h[8:12], h[12:16], h[16:20], h[20:])


native_types = {
  "friend_id":    (parse_friend_id,    2),
  "bytestring":   (parse_bytestring,   2),
  "timestamp_s":  (parse_timestamp_s,  0),
  "timestamp_ms": (parse_timestamp_ms, 0),
  "raw_uuid":     (parse_raw_uuid,     2),
}
