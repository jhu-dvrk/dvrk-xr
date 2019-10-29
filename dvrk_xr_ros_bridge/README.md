dvrk-xr-ros-bridge
===
The python program subscribes ros messages published by multiple dvrk robot arm topics (e.g. /dvrk/PSM1/state_joint_current, /dvrk/PSM2/state_jaw_desired, ...) in the dvrk console, extracts and converts the messages using json format, and send the json message to unity xr application using UDP protocol. 

Usage
===
**Step one: Run ``dvrk_console_json`` application** 

Run the dVRK console application that sends ros messages to dVRK ROS topics. Follow the instructions of starting the dVRK console application the listed in this link [https://github.com/jhu-dvrk/dvrk-ros/tree/master/dvrk_python](https://github.com/jhu-dvrk/dvrk-ros/tree/master/dvrk_python). 

CAUTION: For the following two commands in the preceding instructions:

 - ``p.dmove_joint(numpy.array([0.0, 0.0, -0.05, 0.0, 0.0, 0.0, 0.0]))``
 - ``p.move_joint(numpy.array([0.0, 0.0, 0.10, 0.0, 0.0, 0.0, 0.0]))``

Fill in **6** float type values (any values you want) in the bracket in ``numpy.array()``. Otherwise, an array size warning will jepordize the program.

**Step two: Environmental Setup**

 - Make sure ``roscore`` is running in the terminal. You will also need this for starting the dVRK console.
 - Make sure you have sourced setup.bash for your catkin_ws. 

   Type:``source ~/path/to/your/catkin_ws/devel/setup.bash``
 
 
 **Step Three: Run ``dvrk_xr_ros_bridge.py``**
 
 - Change current directory to the directory of ``dvrk_xr_ros_bridge.py``. 
 - Type:``chmod +x dvrk_xr_ros_bridge.py`` to make the python file an executable.
 - Type:``./dvrk_xr_ros_bridge.py [Name of the robot arm] [IP] [PORT]`` to run.

F.Y.I : 

 - ``[Name of the robot arm]`` is the robot arm whose joint state message you want to send to your unity application. 
 - ``[IP]`` is the IP address of the device where you have the unity application installed. You can search for the IP address in WIFI setting page of your device. 
 - ``[PORT]`` is the port number of individuall robot arm stated in unity c# script. 

