This page details software and hardware setup. This will take a few steps, but then you'll be set up to use your ArbotiX:
  * **Install Arduino Software** - the IDE for creating code for our controller.
  * **Install ArbotiX Distribution** - we'll also need to install some files to use the ArbotiX with the Arduino IDE.
  * **Learn About The Connectors** and how to apply power to your board
  * **Test Your Setup** and update pypose sketch at the same time.
  * **Install PyPose** - A simple pose and capture program for the ArbotiX.

# Arduino Software Setup #
```
Arduino is an open-source electronics prototyping platform based on flexible,
easy-to-use hardware and software. -- arduino.cc
```
The ArbotiX software is based on [Arduino](http://www.arduino.cc). The first thing we need to do is to install the Arduino software:
  1. Install the Arduino framework: follow the instructions at http://arduino.cc/en/Main/Software to install Arduino 1.0 or higher.

The rest of this document assumes familiarity with the Arduino environment. See [the Arduino documents](http://arduino.cc) for details on using the Arduino IDE.

# ArbotiX Software Setup #
To use the ArbotiX with the Arduino IDE we need to add some files to our Arduino sketchbook folder.

Most users will want to download the latest **ArbotiX/PyPose** release from the front page, extract the zip file, and copy the contents of the **arbotix** folder into the sketchbook. This includes the **hardware** folder, **libraries** folder and a number of example sketches.

Alternatively you can checkout the absolute latest, bleeding edge source from our SVN repository, and then locate the files correctly as described above.

# Connecting Power, Etc #
Please see the downloadable ArbotiX manual for instructions and guidance in connecting external devices and power to the board. Although all boards ship with the _pypose_ sketch already installed, we recommend always upgrading to the newest version, in case changes have been made since your board was produced.

See the [RX-Bridge](RxBridge.md) page for details on setting up an RX Bridge.

# Upload PyPose Sketch #
Now, let's test our Arduino installation and programmer. Before PyPose can interact with our robot, we need to download a program (or a _sketch_ as the Arduino environment calls them) onto the ArbotiX. The "pypose" sketch provides a pass through from the ArbotiX to the Bioloid bus, by speaking the correct protocol with PyPose.

Open the Arduino IDE, from **File -> Open** select the PyPose sketch. From the **Tools -> Board** menu, select **ArbotiX** board to make sure all went well above. Connect your board via either the ISP or FTDI cable, select the correct port, and **Upload** it. While we ship each board with a version of pypose installed, it may not be the latest. _Please Note: An FTDI cable should not be connected at the same time as an XBEE radio is in the board. Always remove the XBEE radio before connecting an FTDI cable_

Any time you load your own code onto the board, it will overwrite the pypose sketch, so you'll have to upload it before using pypose again.

### Uploading with an ISP ###
If you want to use an In-System Programmer (ISP), the usage has changed in Arduino 1.0. You now use **File->Upload using Programmer** and no longer have to manually edit files! The Arduino environment now includes a number of supported programmers, but we have added one for the Pololu Serial ISP which shows up as **AVRISP mkII (serial)**.

### Wireless Uploading ###
With a bootloader on the ArbotiX, you can do wireless uploading. The ArbotiX bootloader runs at a 38400 baud rate, so your XBEE radios need to be set to 38400 for wireless downloading. You'll also have to manually push the RESET button. A tutorial on getting around the reset button push is here: http://www.ladyada.net/make/xbee/arduino.html

_Note: wireless uploading is dangerous, if you experience RF-interference something may go wrong. We do not recommend doing this unless you have an ISP to restore the bootloader, and also have enough experience to know how to restore the bootloader._

# PyPose Setup #
PyPose is a pose and capture program, written in Python using wxPython. We of course will have to install Python, wxPython, PySerial to access serial ports, and then PyPose itself.
  1. Download and install Python 2.x: http://www.python.org/download/releases/
  1. Download and install wxPython: http://www.wxpython.org/download.php
  1. Download and install PySerial: http://sourceforge.net/projects/pyserial/files/
  1. Put the PyPose software in an easy to use location, and start pypose.py to run PyPose.

If using Ubuntu, you can install items 1-3 of the above with: _sudo apt-get install python python-serial  python-wxgtk2.8_.

# Connect with PyPose #
PyPose communicates over a serial link to the board, either through an FTDI cable or XBEEs. If using XBEEs, they must be set to 38400, and should be paired. See the [XBEE tutorial](http://forums.trossenrobotics.com/tutorials/how-to-diy-128/xbee-basics-3259/) on TRC for details:

Congratulations, your ArbotiX and PyPose are setup! Now you can go to the PyPose documentation page to start interacting with your robot.