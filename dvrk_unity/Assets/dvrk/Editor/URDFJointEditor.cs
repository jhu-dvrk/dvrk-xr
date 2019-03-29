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
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using DVRK;

[CustomEditor(typeof(URDFJoint))]
[CanEditMultipleObjects]
public class URDFJointEditor : Editor {
    public SerializedProperty RPY, XYZ, jointType, jointAxis, jointObject, defaultJointValue, independent, jointLimit, mimicFactor, mimicParent;

    public void OnEnable() {
        RPY = serializedObject.FindProperty("RPY");
        XYZ = serializedObject.FindProperty("XYZ");
        jointType = serializedObject.FindProperty("jointType");
        jointAxis = serializedObject.FindProperty("jointAxis");
        jointObject = serializedObject.FindProperty("jointObject");
        jointLimit = serializedObject.FindProperty("jointLimit");
        defaultJointValue = serializedObject.FindProperty("defaultJointValue");
        independent = serializedObject.FindProperty("independent");
        mimicFactor = serializedObject.FindProperty("mimicFactor");
        mimicParent = serializedObject.FindProperty("mimicParent");
    }



    public override void OnInspectorGUI() {
        serializedObject.Update();

        EditorGUILayout.PropertyField(RPY, new GUIContent("Rotation (RPY)"));
        EditorGUILayout.PropertyField(XYZ, new GUIContent("Translation (XYZ)"));
        EditorGUILayout.PropertyField(jointType, new GUIContent("Joint Type"));

        int jointTypeValue = jointType.enumValueIndex; // Fixed, Revolute, Continuous, Prismatic
        if (jointTypeValue == 0) { // Fixed
            ;
        }
        else if (jointTypeValue == 1) { // Revolute
            EditorGUILayout.PropertyField(jointObject, new GUIContent("Joint Object"));
            EditorGUILayout.PropertyField(jointAxis, new GUIContent("Joint Axis"));
            EditorGUILayout.PropertyField(jointLimit, new GUIContent("Joint Limit"));
            EditorGUILayout.PropertyField(independent, new GUIContent("Indenpendent Joint"));
            bool independentValue = independent.boolValue;
            if (independentValue) {
                EditorGUILayout.PropertyField(defaultJointValue, new GUIContent("Default Joint Value"));
            }
            else {
                EditorGUILayout.PropertyField(mimicParent, new GUIContent("Mimic Parent Joint"));
                EditorGUILayout.PropertyField(mimicFactor, new GUIContent("Mimic Factor"));
            }
        }
        else if (jointTypeValue == 2) { // Continuous
            EditorGUILayout.PropertyField(jointObject, new GUIContent("Joint Object"));
            EditorGUILayout.PropertyField(jointAxis, new GUIContent("Joint Axis"));
            EditorGUILayout.PropertyField(independent, new GUIContent("Indenpendent Joint"));
            bool independentValue = independent.boolValue;
            if (independentValue) {
                EditorGUILayout.PropertyField(defaultJointValue, new GUIContent("Default Joint Value"));
            }
            else {
                EditorGUILayout.PropertyField(mimicParent, new GUIContent("Mimic Parent Joint"));
                EditorGUILayout.PropertyField(mimicFactor, new GUIContent("Mimic Factor"));
            }
        }
        else if (jointTypeValue == 3) { // Prismatic
            EditorGUILayout.PropertyField(jointObject, new GUIContent("Joint Object"));
            EditorGUILayout.PropertyField(jointAxis, new GUIContent("Joint Axis"));
            EditorGUILayout.PropertyField(jointLimit, new GUIContent("Joint Limit"));
            EditorGUILayout.PropertyField(independent, new GUIContent("Indenpendent Joint"));
            bool independentValue = independent.boolValue;
            if (independentValue) {
                EditorGUILayout.PropertyField(defaultJointValue, new GUIContent("Default Joint Value"));
            }
            else {
                EditorGUILayout.PropertyField(mimicParent, new GUIContent("Mimic Parent Joint"));
                EditorGUILayout.PropertyField(mimicFactor, new GUIContent("Mimic Factor"));
            }
        }




        serializedObject.ApplyModifiedProperties();
    }
}
