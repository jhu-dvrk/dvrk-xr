#!/usr/bin/env python

import rospy
import json
import socket
import sys
import message_filters
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from pyparsing import *

def joint_state_msg(time, name, position, velocity, effort):
    # build json formatted string
    msg = "\"GetStateJoint\": {\n\t\"AutomaticTimestamp\": true,\n\t\"Effort\": " + effort + ",\n\t\"Name\": [" + name + "],\n\t\"Position\": " + position + ",\n\t\"Timestamp\": " + time + ",\n\t\"Type\": [2,2,1,2,2,2]" + ",\n\t\"Valid\": true,\n" + "\t\"Velocity\": " + velocity + "}\n"

    return msg

#---------------------------------------

def jaw_state_msg(time, name, position, velocity, effort):
    # build json formatted string
    msg = "\"GetStateJaw\": {\n\t\"AutomaticTimestamp\": true,\n\t\"Effort\": " + effort + ",\n\t\"Name\": [" + name + "],\n\t\"Position\": " + position + ",\n\t\"Timestamp\": " + time + ",\n\t\"Type\": [0]" + ",\n\t\"Valid\": true,\n" + "\t\"Velocity\": " + velocity + "}\n"

    return msg

#---------------------------------------

def extract_joint_data(data):
    # set literal limit
    ParserElement.setDefaultWhitespaceChars(' \t')  
    time = Literal("nsecs: ")
    name = Literal("- ")
    position = Literal("position: ")
    velocity = Literal("velocity: ")
    effort = Literal("effort: ")
    end_of_line = LineEnd()
    word = Word(printables)

    # build pattern
    p1 = time + OneOrMore(word) + end_of_line      
    p2 = name + OneOrMore(word) + end_of_line
    p3 = position + OneOrMore(word) + end_of_line
    p4 = velocity + OneOrMore(word) + end_of_line
    p5 = effort + OneOrMore(word) + end_of_line
 
    # extract data
    time_data = p1.searchString(str(data))         
    name_data = p2.searchString(str(data))
    position_data = p3.searchString(str(data))
    velocity_data = p4.searchString(str(data))
    effort_data = p5.searchString(str(data))
    
    #connect data
    time_json = time_data[0][1]
    name_json = "\"" + name_data[0][1] + "\", \"" + name_data[1][1] + "\", \"" + name_data[2][1] + "\", \"" + name_data[3][1] + "\", \"" + name_data[4][1] + "\", \"" + name_data[5][1] + "\""
    position_json = position_data[0][1] + position_data[0][2] + position_data[0][3] + position_data[0][4] + position_data[0][5] + position_data[0][6]
    velocity_json = velocity_data[0][1] + velocity_data[0][2] + velocity_data[0][3] + velocity_data[0][4] + velocity_data[0][5] + velocity_data[0][6]
    effort_json = effort_data[0][1] + effort_data[0][2] + effort_data[0][3] + effort_data[0][4] + effort_data[0][5] + effort_data[0][6]

    #generate joint state data
    return joint_state_msg(time_json, name_json, position_json, velocity_json, effort_json)

#---------------------------------------

def extract_jaw_data(data):
    # set literal limit
    ParserElement.setDefaultWhitespaceChars(' \t')  
    time = Literal("nsecs: ")
    name = Literal("- ")
    position = Literal("position: ")
    velocity = Literal("velocity: ")
    effort = Literal("effort: ")
    end_of_line = LineEnd()
    word = Word(printables)

    # build pattern
    p1 = time + OneOrMore(word) + end_of_line      
    p2 = name + OneOrMore(word) + end_of_line
    p3 = position + OneOrMore(word) + end_of_line
    p4 = velocity + OneOrMore(word) + end_of_line
    p5 = effort + OneOrMore(word) + end_of_line
 
    # extract data
    time_data = p1.searchString(str(data))         
    name_data = p2.searchString(str(data))
    position_data = p3.searchString(str(data))
    velocity_data = p4.searchString(str(data))
    effort_data = p5.searchString(str(data))
    
    #connect data
    time_json = time_data[0][1]
    name_json = "\"" + name_data[0][1] + "\""
    position_json = position_data[0][1]
    velocity_json = velocity_data[0][1]
    effort_json = effort_data[0][1]

    #generate joint state data
    return jaw_state_msg(time_json, name_json, position_json, velocity_json, effort_json)

#---------------------------------------

def send_json(msg):
    # generate finalized json file
    x = json.loads(msg)
    finalized_msg = json.dumps(x)		 

    UDP_IP = sys.argv[2]
    UDP_PORT = int(sys.argv[3])

    # Sending message to UDP_IP at UDP_PORT
    
    # creat socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
    
    # send message
    sock.sendto(str.encode(finalized_msg), (UDP_IP,UDP_PORT))      

    #print('Message Sent')

    sock.close

#---------------------------------------

def callback(jaw_raw, joint_raw):
    # process raw jaw and joint data
    jaw_string_msg = extract_jaw_data(jaw_raw)
    joint_string_msg = extract_joint_data(joint_raw)

    # generate json string 
    json_msg = "{\n" + jaw_string_msg + ",\n" + joint_string_msg + "}"

    # call send message function
    send_json(json_msg)

#---------------------------------------

def joint_server(joint_raw):
    # process raw jaw data
    joint_string_msg = extract_joint_data(str(joint_raw))

    # generate json string 
    json_msg = "{\n" + joint_string_msg + "}"

    # call send message function
    send_json(json_msg)

#---------------------------------------

def bridge():
    rospy.init_node('udp_bridge', anonymous=True)
    # subscribing
    if (sys.argv[1] == "PSM1" or sys.argv[1] == "PSM2"):
	jaw_raw = message_filters.Subscriber("/dvrk/" + sys.argv[1] + "/state_jaw_current", JointState)
	joint_raw = message_filters.Subscriber("/dvrk/" + sys.argv[1] + "/state_joint_current", JointState)
	ts = message_filters.ApproximateTimeSynchronizer([jaw_raw, joint_raw], 10, 1, allow_headerless=True)
	ts.registerCallback(callback)
    elif (sys.argv[1] == "MTML" or sys.argv[1] == "MTMR" or sys.argv[1] == "ECM"):
	rospy.Subscriber("/dvrk/" + sys.argv[1] + "/state_joint_current", JointState, joint_server)
    else:
    # invalid dvrk actuators, print error 
	print('Invalid actuator, topic not found.')         
    rospy.spin()

#---------------------------------------

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: rosrun bridge [PSM1 | PSM2 | MTML | MTMR | ECM] [IP] [PORT]')
        sys.exit

    bridge()


