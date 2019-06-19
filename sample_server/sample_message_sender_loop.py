import json
import sys
import socket
import time

if len(sys.argv) < 4:
    print('Usage: python sample_message_sender_loop.py FILE [IP] [PORT]')
    sys.exit()

if not sys.argv[1].endswith('.traj'):
    print('Please use the trajectory file ends with .traj')
    sys.exit()

jointStates = []
with open(sys.argv[1]) as jointFile:
    for line in jointFile:
        d = json.loads(line)
        jointStates.append(json.dumps(d))

UDP_IP = sys.argv[2]
UDP_PORT = int(sys.argv[3])

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

for j in jointStates:
    sock.sendto(str.encode(j), (UDP_IP, UDP_PORT))
    time.sleep(0.01)

sock.close()

