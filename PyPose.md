# Introduction #
One of the most important features of AX-12 servos is that we can move the servo to a particular position by hand and read the position back from the servo. This feature allows us to _pose_ the robot, and _capture_ the pose. PyPose began as a simple open-source pose and capture program, written in Python and using wxPython for a graphical package. Traditionally, roboticists might create a series of poses, and then assemble them into a _motion sequence_.

As has often been said, there is more than one way to solve any problem. Motion sequences can be created extremely quickly using PyPose, but they do have limitations:
  * Poses are not dynamic: given a limited number of poses, you have a limited number of positions the body can go to.
  * Sequence creation can become quite repetitive if you desire a higher degree of control of the robot.

The logical improvement is to _parameterize_ the poses. By adding or subtracting the value of a dynamic parameter we can vary the response of our poses and motion sequences far more than before. This can [easily be done in software](BioloidController#Walking_with_Fewer_Poses.md) after you export.

Of course, the holy grail of motion control is to have a fast Inverse Kinematics engine. Using inverse kinematics, we can compute how to place the foot of a robot into any position it can physically occupy. The _Nearly Universal Kinematics Engine_, or NUKE, is a highly templated IK solution for quadrupeds and hexapods. After answering a series of questions about the construction of the robot, we can automatically build an IK engine for the robot. Why then would we even offer poses and sequences?
  * NUKE still has a limited number of configurations it can handle, if you are building something like a biped you will _have_ to use poses.
  * IK can be slow. If you have other important code to run, you may not be able to run a full IK engine.

Regardless of the method of motion creation, PyPose exports your work directly into C code that can be loaded onto the arbotiX using the Arduino IDE. PyPose also has a Terminal for editing servo parameters.

<div>
<h1>Hardware Setup</h1>
See the GettingSetup page<br>
<br>
</div>
# Getting Started #
We can finally start PyPose, the initial view will look something like this:

<img src='http://arbotix.googlecode.com/svn/wiki/pypose.png'>

<i><b>Figure 1 - The PyPose program when first loaded, showing empty pose list and pose editor.</b></i>

This default view is the <i>Pose Editor</i>, one of the many tools in PyPose. There is a menu bar across the top of the program at all times, and a status bar across the bottom of the window. The left hand side of the status bar prompts you with <i>please create or open a project</i>. The right hand side of the status bar shows our connection status, telling us that we are currently not connected to a robot. The <b>tools</b> menu is probably the most important, as it lets us switch between the <i>Pose Editor</i>, <i>Sequence Editor</i>, <i>NUKE</i>, and other tools:<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/toolsmenu.png'>

<h1>Creating a New Robot, Connecting to the arbotiX</h1>
The first thing we need to do is to create a project. A project is where we will store our poses, sequences, and IK/FK configurations. Click on <b>project|new</b> in the menu, and the <b>Create New Project</b> dialog will appear. Enter the name of your robot, and the number of servos used. <i>Note: currently, servos must be number sequentially, if you have 12 servos, they must be ID1 to ID12, you can change the ID of a servo using the Servo Terminal.</i> We are now ready to begin actually talking with our robot. You can repeatedly save and open project files.<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/newproj.png'>
<img src='http://arbotix.googlecode.com/svn/wiki/serial.png'>

<i><b>Figure 2 - Create New Project and Select Communications Port windows.</b></i>

To communicate with our robot, we need open a port to our XBEE explorer, or FTDI board. You can open a port by clicking on <b>config|port</b> in the menu, and selecting a port name in the <b>Select Communications Port</b> box that will pop up (shown above). While PyPose will find most serial ports, there is a chance that it cannot automatically detect your port. If this happens, use the instructions on the <i>serial</i> command below to open a port through the Terminal.<br>
<br>
The default baud rate for the arbotiX is 38400bps, if you are using XBEE radios, be sure they are paired, and set to 38400bps. A tutorial on setting up XBEE radios can be found at the <a href='http://forums.trossenrobotics.com/tutorials/how-to-diy-128/xbee-basics-3259/'>Trossen Robotic Community</a>.<br>
<br>
<h1>The Pose Editor</h1>
Once you have created a robot, PyPose will adjust to show the correct number of sliding servo adjustment bars. The box to the right of the adjustment bars displays the names of poses we have captured, since we haven't captured any, it will be blank. Below the pose list, we have two buttons: <i>add</i> and <i>remove</i>, for creating a new pose or deleting one. Click on <i>add</i> and enter a name for your pose. For instance, I typically create a pose named "stand", for the default standing position of my bot. If you click on a pose in the list, it's servo values are loaded into the slider bars.<br>
<br>
We also have 4 buttons underneath our servo adjustment bars: <i>delta-T</i>, <i>relax</i>, <i>capture</i>, and <i>set</i>. <b>relax</b> shuts of the servo torque, allowing you to pose the robot into place. <b>set</b> will write the current servo adjustment bar values out to the robot's servos. If during a <b>set</b> operation, the servos were to move too fast, the robot or operator could be injured. The <b>delta-T</b> button brings up a dialog to select how long transitions take. This time defaults to 500ms, or half a second.<br>
<br>
<b>capture</b> allows us to read the values into the slider bars. When you click <b>capture</b>, a status indicator will appear:<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/capture.png'>

<i><b>Figure 3 - capture status bar.</b></i>

It should disappear quite quickly, unless PyPose has trouble reading a servo. When complete, the lower left corner of the status bar will either say <i>"capture done!"</i> to indicate success, or list a set of servos it could not query. If you have trouble, check to make sure that you have entered the correct number of servos during robot setup, and that all of your wires are tight. Old wires may have to be replaced.<br>
<br>
Servo values can be manually edited after a capture, just move the sliding adjustment bars. The left and right arrow keys can be used to fine tune the values. Using the <i>shift</i> key and the left and right arrows you can jump large amounts.<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/pypose2.png'>

<i><b>Figure 4 - PyPose, after a successful capture.</b></i>

<i>Note: Be careful when clicking</i> capture, <i>as it will overwrite any data attached to the pose currently selected in the pose list. We are currently revamping the pose interface to be more data safe!</i>

There are several keyboard accelerators for the PyPose Pose Editor:<br>
<ul><li>Ctrl-A - advance to a new pose, this creates a default name for a new pose and then selects the pose.<br>
</li><li>Ctrl-C - capture to the current pose.<br>
</li><li>Ctrl-R - relax servos</li></ul>

<h1>The Sequence Editor</h1>
Selecting <b>tools|sequence editor</b> will display the sequence editor instead of the pose editor. The sequence editor, shown below in <i>figure 5</i> contains a group of controls dedicated to editing an individual sequence and a list of sequences on the right side of the screen. Below the sequence editor are four buttons: <i>relax</i>, <i>run</i>, <i>loop</i>, and <i>halt</i>. <b>relax</b> works just like it did in the pose editor. <b>run</b>, <b>loop</b> and <b>halt</b> will start and stop the sequence you are currently editing from running. <b>run</b> runs the sequence through one iteration or until a <b>halt</b> is received, <b>loop</b> will cause the sequence to run until a <b>halt</b> command is received. The download of a sequence to the arbotiX may take a few moments. Below the list of sequences are two buttons: <i>add</i> and <i>remove</i> for creating and deleting sequences.<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/sequence.png'>

<i><b>Figure 5 - PyPose, sequence editor tool.</b></i>

A sequence is simply a compilation of transitions that will be played in order (from the top of the transition box to the bottom of the box). Each transition consists of a pose to transition to, and a time to take during the transition denoted as <i>delta-T</i>. The <b>new</b> and <b>delete</b> buttons can be used to add new transitions or delete existing ones. Each new transition added to the box has a default pose of <i>none</i> and a time of <i>500ms</i> (1/2 of a second). The <b>move up</b> and <b>move down</b> buttons can be used to rearrange transitions.<br>
<br>
<h1>Exporting to the AVR</h1>
Selecting <b>tools|export to AVR</b> will allow you to save a C header file, which contains all of your poses and sequences, in a format that stores them in FLASH memory, and makes them available to the BioloidController.<br>
<br>
<h1>Servo Terminal</h1>
The servo terminal is a useful tool for configuring servos that are connected to an ArbotiX or USBDynamixel. It currently implements only a subset of it's eventual commands. It can currently be used to query an ArbotiX to find out what servos are attached, or to change the ID number of a servo:<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/terminal.png'>

<i><b>Figure 6 - PyPose Terminal, showing a sequence of edits.</b></i>

Figure 6 shows a typical interaction with the Terminal. We need to remember to open the port. The user then typed <i>help</i> to see commands, then <i>ls</i> to see the servos and found out that servos 1,2,3,4 were attached. They then changed servo 4's ID to 5. Now, when listing the servos with <i>ls</i>, they got 1, 2, 3, and 5. Finally, they changed servo 5 back to ID4 and ran <i>ls</i> one final time to be sure all went good.<br>
The current command list is as follows:<br>
<ul><li>ls - list the servos attached to an ArbotiX.<br>
</li><li>mv current_id new_id - renumber a servo<br>
</li><li>serial port_name - open a serial port. <i>ex: serial /dev/ttyUSB0</i>
</li><li>help - access help menu<br>
Commands that are still under development:<br>
</li><li>ls baud - list, with baud rate change<br>
</li><li>set param index value - set a parameter (position, speed, tuning)<br>
</li><li>get param index - get a parameter (position, speed, temp, tuning)</li></ul>

<h1>Hacking</h1>
Robot pose files are plain text. The format is quite simple, the first line is the robot name and servo count, separated by a colon. Each line after that should be a pose or sequence. A pose is composed of a name, colon, and then the servo values. A sequence has a name, followed by a colon, and then a list of pairs of pose names and transition times.<br>
<pre><code>myNewRobot:4<br>
Pose=pose1: 512, 512, 512, 512 <br>
Pose=poseX: 92, 104, 92, 800<br>
Seq=myFirstSequence: pose1|1000, poseX|500, pose1|800<br>
</code></pre>

The communications protocol used by PyPose and the sketch on your arbotiX is essentially the same as the Bioloid bus itself. We have, however, defined additional registers, and an ID of 253 will command the arbotiX to act on these special registers, which allows things like pose and sequence upload and live playback.