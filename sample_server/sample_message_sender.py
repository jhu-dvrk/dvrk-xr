#!/usr/bin/env python

# Author: Long Qian
# Date: 2019-03-29

# (C) Copyright 2019 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---

# Send a sample message to a destination IP:PORT using UDP
# > python sample_message_sender.py FILE [IP] [PORT]


import json
import sys
import socket

if len(sys.argv) < 4:
	print('Usage: python sample_message_sender.py FILE [IP] [PORT]')
	sys.exit()

s = ""
with open(sys.argv[1]) as json_data:
    d = json.load(json_data)
    s = json.dumps(d) 
    

UDP_IP = sys.argv[2]
UDP_PORT = int(sys.argv[3])

print('Sending message to ' + UDP_IP + ':' + str(UDP_PORT))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(str.encode(s), (UDP_IP, UDP_PORT))

print('Message sent')

sock.close()

