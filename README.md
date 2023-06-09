# Snapchat Message Database Reader

Passively read messages from Snapchat Android databases. This has worked since
at the latest 2021 and works as of 20230609 for groups as well as individual conversations.
As protocol buffers are [designed with forward-compatibility](https://protobuf.dev/overview/#updating-defs)
in mind, it is unlikely that this will stop working for quite a while.
<center><img src=snapreader.png></center>

On Android, Snapchat stores all messages, read or not, in a binary field containing a
protobuf message in a SQLite3 database.
Using [protobuf-inspector](https://github.com/mildsunrise/protobuf-inspector), I reversed the
message format so I could get a readout of Snapchat messages in my terminal.

## Usage

### Relevant Files
To read messages yourself, you will need to copy the following files from your phone.
This will almost certainly require root access.
``` sh
/data/data/com.snapchat.android/databases/arroyo.db*  # messages
/data/data/com.snapchat.android/databases/main.db*    # contacts
```
Temporary files (`*-shm`, `*-wal`) can be cleaned up with
``` sh
$ sqlite3 arroyo.db 'vacuum;'
```

### Dumping Contacts
To dump your contact/friend data to a JSON file, run
``` sh
$ python research/dump-contacts main.db
```

### Displaying a Conversation
To actually display a conversation, you'll need the `conversation_client_id` associated with it.
Browse the `conversation` table in `arroyo.db` with `sqlite3` or [`sqlitebrowser`](https://sqlitebrowser.org/)
to find the appropriate UUID.

Once you have your `contacts.json` and client conversation id, simply run
``` sh
$ python -m snapreader arroyo.db contacts.json <CCID>
```

## Further Reversing
I've only reversed and implemented the bare minimum subset of the conversation message protobuf description
necessary for my own ends. If you'd like to continue reversing where I left off, install [protobuf-inspector](https://github.com/mildsunrise/protobuf-inspector) and dump all your message content blobs with [`research/dump-message-blobs`](research/dump-message-blobs). Then, in the same directory as `protobuf_config.py`, run

``` sh
$ protobuf_inspector < BLOB_PATH
```
<center><img src=inspector.png></center>

Read more about the process on the `protobuf-inspector` homepage. After identifying more fields, you can update
`content.proto`, an actual protobuf message definition and compile it for any language with `protoc`.

You can also find already-decrypted picture and video snaps here:
``` sh
/data/data/com.snapchat.android/files/native_content_manager/* # decrypted snap videos/images
```
