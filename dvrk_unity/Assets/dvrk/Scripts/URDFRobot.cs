/*
    Author(s):  Long Qian
    Created on: 2019-03-29
    (C) Copyright 2015-2018 Johns Hopkins University (JHU), All Rights Reserved.

    --- begin cisst license - do not edit ---
    This software is provided "as is" under an open source license, with
    no warranty.  The complete license can be found in license.txt and
    http://www.cisst.org/cisst/license.txt.
    --- end cisst license ---
*/
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace DVRK {

    public class URDFRobot : MonoBehaviour {

        public List<URDFJoint> independentJoints = new List<URDFJoint>();
        public URDFJoint jaw = null;

        public static List<URDFRobot> instances = new List<URDFRobot>();
        private int instanceID = -1;

        private UDPClient udpClient;

        public virtual void HandleMessage(string message) {
            Debug.Log("DVRK::URDFRobot base class not implementing HandleMessage");
        }


        // Use this for initialization
        void Start() {
            // all the joints, to setup linkage
            foreach (URDFJoint joint in GetComponentsInChildren<URDFJoint>()) {
                joint.SetupRobotJoint();
            }
            foreach (URDFJoint joint in independentJoints) {
                joint.SetJointValueDefault();
            }
            if (jaw != null) {
                jaw.SetJointValueDefault();
            }
            
            udpClient = GetComponent<UDPClient>();

            instances.Add(this);
            instanceID = instances.Count - 1;
            Debug.Log(name + ": Current URDFRobot instanceID: " + instanceID);
        }

        // LateUpdate is called once per frame
        void LateUpdate() {
            string message = "";
            message = udpClient.GetLatestUDPPacket();

            if (message != "") {
                HandleMessage(message);
            }
        }
        
        

#if UNITY_EDITOR
        void OnGUI() {
            int width = 100;
            int height = 20;
            int currentHeight = height;
            int setupHeight = 20;
            foreach (URDFJoint joint in independentJoints) {
                GUI.Label(new Rect(10 + instanceID * width, currentHeight, width, height), joint.name);
                currentHeight += setupHeight;
                float val = joint.defaultJointValue;
                if (joint.jointType == URDFJoint.JointType.Revolute || joint.jointType == URDFJoint.JointType.Prismatic) {
                    val = GUI.HorizontalSlider(new Rect(10 + instanceID * width, currentHeight, width, height), joint.currentJointValue,
                        joint.jointLimit.x, joint.jointLimit.y);
                }
                else if (joint.jointType == URDFJoint.JointType.Continuous) {
                    val = GUI.HorizontalSlider(new Rect(10 + instanceID * width, currentHeight, width, height), joint.currentJointValue,
                        -180f, 180f);
                }
                joint.SetJointValue(val);
                currentHeight += setupHeight;
            }
            if (GUI.Button(new Rect(10 + instanceID * width, currentHeight, width, height), "Recenter")) {
                foreach (URDFJoint joint in independentJoints) {
                    joint.SetJointValueDefault();
                }
            }
        }
#endif

    }
}
