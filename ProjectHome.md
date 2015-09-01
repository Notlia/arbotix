<h1>ArbotiX RoboController</h1>

<img src='http://www.trossenrobotics.com/store/i/is.aspx?path=/images/PImages/arbotix.jpg' align='right' />

The ArbotiX robocontroller is an Arduino compatible microcontroller board, designed to control small-to-medium sized robots, especially walkers that use Bioloid AX-12 servos.

Support is typically handled through our [discussion forum](http://groups.google.com/group/robocontroller). You can purchase an ArbotiX from [Trossen Robotics](http://www.trossenrobotics.com/p/arbotix-robot-controller.aspx). For more information, visit our website at http://www.vanadiumlabs.com/arbotix or Fergy's blog at http://www.showusyoursensors.com/

## News ##
  * 2-16-11 - ArbotiX/PyPose/NUKE 0014 is now out. This fixes several bugs found in the commander.py controller, and includes an updated BioloidController library (required for ROS support).

## Hardware Specifications ##
The ArbotiX sports an 16Mhz ATMEGA644P, with 64k of flash ROM, and 4k of RAM. It has 2 serial ports, 1 dedicated to Bioloid servo controller, the other to the XBEE radio. A total of 32 I/O, 8 of which can function as analog inputs with servo style 3-pin headers (gnd, vcc, signal) on all 8 analog inputs, and 8 of the digital IO. The ArbotiX has dual 1A motor drivers, with combined motor/encoder header. ArbotiX is 2.8”x2.8” with mounting holes designed to match many Bioloid configurations.

## Software ##
A number of software programs have been designed to make working with your ArbotiX quite easy:
  * BioloidController - this is a Bioloid bus library for use with the Arduino/Sanguino environment. It allows easy manipulation of poses, the storage of poses in FLASH, and full interaction with AX-12 servos.
  * PyPose - this is the stock pose & capture software. Written in Python, uses pySerial to communicate with an arbotiX board running the pypose sketch. After you have done pose and capture, PyPose can automatically create a C header file with the poses ready to load with the Bioloid Library.
  * OtherLibraries - there are several other, smaller, libraries that have been made to make using the arbotiX extremely easy.

## Sample Programs ##
Each sample program is an Arduino sketch, held in it's own directory within the _Sketches_ directory of the release. Current examples include:

<table cellpadding='5' border='1'>
<tr><td>IssyDunnYet</td><td>the ArbotiX was originally designed for IssyDunnYet, the 2009 Gold Medalist in Mech Warfare. We've updated Issy's code to fix several bugs and to use the newer BioloidController library. The sketch directory also contains PyMech which is the Python-based console for controlling Issy. </td></tr>
<tr><td>Droid</td><td>is an example of how to use this software with the Walking Droid found in the Bioloid Beginner kit. A video should be posted shortly. </td></tr>
<tr><td>I2C Sonar <code>*</code></td><td>How to use an SRF-02 sonar with the ArbotiX.</td></tr>
<tr><td>DiffDrive <code>*</code></td><td>How to use the motor and encoder headers of the ArbotiX to implement closed loop control of a differential drive robot.</td></tr>
<tr><td>pypose</td><td>is the pass through program for interacting with PyPose</td></tr>

</table>

A `*` denotes examples coming soon.
_note: eventually, most of these examples will have their own page describing the example._

## Licensing ##
All of the ArbotiX libraries, robocontroller libraries, and Arduino extensions are licensed under the GNU Lesser General Public License v2.1. PyPose, and any other desktop software included (such as PyMech), is released under the GNU General Public License v2.