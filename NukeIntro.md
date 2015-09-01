# NUKE - The Nearly Universal Kinematics Engine #

The Nearly Universal Kinematics Engine (NUKE) is an easy to use PyPose tool that creates a customized Inverse Kinematics solution and gait engine for your ArbotiX-powered robot. It works for most popular configurations of quadrupeds and hexapods.

Most of this documentation overlaps with our introductory video:

<a href='http://www.youtube.com/watch?feature=player_embedded&v=biA7AhWRvpU' target='_blank'><img src='http://img.youtube.com/vi/biA7AhWRvpU/0.jpg' width='425' height=344 /></a>

## How To Use NUKE ##

Be sure to create a robot project, and specify the number of servos before working with NUKE. This can be done exactly the same way as it was in PyPose when you were just using poses and sequences. Next, select **Tools|Nuke** to load the NUKE editor. Most of the editor will be disabled until you select the type of IK configuration and number of legs on your robot.

<img src='http://arbotix.googlecode.com/svn/wiki/nuke.png'>

<i><b>Figure 1 - NUKE editor.</b></i>

After selecting the type of IK and number of legs, you'll want to input the lengths of the robot's body and leg segments on the left side of the editor. Images to the side of the parameters  shows what to measure. <a href='Hidden comment: Clicking on *Help* will bring up a dialog showing you what to measure, some of the measurements are dependent on the type of IK selected.'></a> The next step is to select the servo mapping (which servo ID corresponds to which servo in the robot) on the right side of the editor.<br>
<br>
We're now setup to capture the really important values. The first thing to capture is the minimum and maximum values of each servo, the points where the servo would collide with the body. Click the button for <b>Capture Limits</b> and PyPose will ask you to step through and move each servo to it's extremes. PyPose automatically will configure which end is a minimum and which is a maximum. <b>Be careful</b> with this step, make sure that you don't rotate the servo past it's 0-300 degree range, or your minimum and maximum values will be wrong.<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/neutral.png'>

<i><b>Figure 2 - Neutral capture dialog for 3DOF lizard-style legs.</b></i>

The next step is to capture the neutral position. This will vary a bit depending on the type of IK you are using, but when you click on <b>Capture Neutral</b> a dialog will be presented with a picture showing where your robot's legs should be placed. This pose will be saved as <i>ik_neutral</i>, and can be edited inside the Pose Editor if needed.<br>
<br>
The last step in initial setup is the sign test. We need to make sure our IK engine moves legs in the correct direction depending on how our servos are attached. Clicking <b>Do Sign Test</b> will send us through a series of questions like "Did my left front leg move forward?". Make sure your bot is free to move (either hold it carefully, or have a stand for it).<br>
<br>
<h2>Gait Configuration</h2>

At this time, no gait configuration is needed. NUKE automatically picks a default stance that should be effective. For information about how to improve performance, particularly range of motion and speed of walking, see NukeTuning.<br>
<br>
<a href='Hidden comment: <font color="#FF0000"> TODO: setup the gait engine and default foot placements 

Unknown end tag for </font>


<font color="#FF0000"> TODO: testing the gait engine 

Unknown end tag for </font>

'></a><br>
<br>
<h2>Export and Testing</h2>

Once the limits, neutrals, and signs are found, it's time to export our sketch. Clicking on <b>Export</b>, NUKE exports a complete sketch, so you'll only need to select a folder in which to put a sketch and support code.<br>
<br>
We now load the sketch inside the Arduino IDE, and download it to the robot. This sketch has a very simple <i>loop()</i> function, which will take serial commands to walk the robot around. Once the sketch is loaded we can use the <b>Test Drive</b> tool within NUKE to control the robot. Test Drive uses the same protocol as the ArbotiX Commander.<br>
<br>
<img src='http://arbotix.googlecode.com/svn/wiki/commander.png'>

<i><b>Figure 3 - ArbotiX Commander Test Drive screen.</b></i>

<h2>Interacting with the IK Engine</h2>
NUKE generates a full inverse kinematics solution and a gait engine for your robot. This is composed of 4 files:<br>
<ul><li><i>nuke.h</i> - header file for IK and gait engine<br>
</li><li><i>nuke.cpp</i> - contains the IK engine<br>
</li><li><i>gaits.h</i> - contains the gait engine<br>
</li><li><i>something.pde</i> - your sketch, the name of the file matches the name of the directory you chose to export to. This is where you'll put the robot's task-related code.</li></ul>

The main loop of your program, in <i>something.pde</i> will look like this:<br>
<pre><code>void loop(){<br>
  // put your task code here<br>
  // make sure it doesn't take too long to execute each cycle<br>
<br>
  if(bioloid.interpolating == 0){<br>
    // last step is done, do the next<br>
    doIK();<br>
    bioloid.interpolateSetup(tranTime);<br>
  }<br>
  bioloid.interpolateStep();<br>
}<br>
</code></pre>

Your code will interact with the gait engine using several global variables, which can be set at any time, from anywhere in your code:<br>
<ul><li><i>Xspeed</i> - the forward speed to walk at, in millimeters/second. Forward is positive.<br>
</li><li><i>Yspeed</i> - the sideways speed to walk at, in millimeters/second. Right is positive.<br>
</li><li><i>Rspeed</i> - the speed to turn at, in radians/second.</li></ul>

The body IK engine also relies on several other variables:<br>
<ul><li><i>bodyPosX</i>, <i>bodyPosY</i> - offset of the center of body in the air, in millimeters.<br>
</li><li><i>bodyRotX</i>, <i>bodyRotY</i>, <i>bodyRotZ</i> - rotation of body about axis, in radians.</li></ul>

<i>doIK()</i> computes the position for each leg, taking into account the gait and body parameters. The interpolation part is documented under the BioloidController library. There is also a default location for each leg, known as the <i>default stance</i>, when the gait and body engines output all zeros. This default stance is found in the <i>setupIK()</i> function of nuke.cpp.