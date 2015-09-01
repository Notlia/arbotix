<h1>ArbotiX RoboController</h1>

<img src='http://www.trossenrobotics.com/store/i/is.aspx?path=/images/PImages/arbotix.jpg' align='right' />

The ArbotiX robocontroller is an Arduino compatible microcontroller board, designed to control small-to-medium sized robots, especially walkers that use Bioloid AX-12 servos.

## Documentation ##
Please read the GettingSetup page to get setup with the ArbotiX.

The ArbotiX project consists of a number of software programs and libraries:
  * PyPose - this is the stock pose & capture software. Written in Python, uses pySerial to communicate with an ArbotiX board running the pypose sketch. After you have done pose and capture, PyPose can automatically create a C header file with the poses ready to load with the Bioloid Library.
  * BioloidController - this is a Bioloid bus library for use with the Arduino/Sanguino environment. It allows easy manipulation of poses, the storage of poses in FLASH, and full interaction with AX-12 servos.
  * OtherLibraries - there are several other, smaller, libraries that have been made to make using the ArbotiX extremely easy.

There are also a number of example programs (which can be found in the _Sketches_ directory of the release):
  * IssyDunnYet - the ArbotiX was originally designed for IssyDunnYet, the 2009 Gold Medalist in Mech Warfare. We've updated Issy's code to fix several bugs and to use the newer BioloidController library. The sketch directory also contains PyMech which is the Python-based console for controlling Issy.
  * Droid - is an example of how to use this software with the Walking Droid found in the Bioloid Beginner kit. A video should be posted shortly.
  * PyPose - is the pass through program for interacting with PyPose.

Additionally, we have created a CodeBook with some commonly requested pieces of code. The ArbotiX can also be used with ROS, see the [vanadium-ros-pkg](http://vanadium-ros-pkg.googlecode.com) repository for details.

Support is typically handled through the [Trossen Robotics Community](http://forums.trossenrobotics.com) Forum. You can purchase an ArbotiX from [Trossen Robotics](http://www.trossenrobotics.com/p/arbotix-robot-controller.aspx).

## Licensing ##
All of the ArbotiX libraries, robocontroller libraries, and Arduino extensions are licensed under the GNU Lesser General Public License v2.1. PyPose, and any other desktop software included (such as PyMech), is released under the GNU General Public License v2.