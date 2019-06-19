Sample Server
===
The sample python server is used to send out messages of joint status, instead of a real robot for debugging purposes.

## Usage
- sample_message_sender.py

```
# send out one message
# FILE can be any .json file in this folder
python sample_message_sender.py FILE IP PORT
```

- sample_message_sender_loop.py

```
# send out a joint trajectory
# FILE can be any .traj file in this folder
python sample_message_sender_loop.py FILE IP PORT
```



