# ArbotiX2 Beta Program Notes #

## Arduino Updates ##
To use the ArbotiX2, you need to update your install just a bit. Please download [the updated libraries and ros firmware](http://code.google.com/p/arbotix/downloads/detail?name=arbotix2-beta.zip&can=2&q=).

Please make sure you have installed the robocontroller libraries, then copy each library folder to your sketchbook/libraries folder (this will replace some of the libraries from the arbotix and robocontroller distributions with newer versions). Copy the ros firmware folder to your sketchbook.

To use the arbotix2 with pypose or ROS, compile and upload the ros firmware using Arduino IDE (yes, while it is called "ros", it's actually a newer more awesome pypose sketch).

## Backwards Compatibility ##
Each of the libraries in the above download are backwards compatible with other ArbotiX-family processors -- however, you must:
  * Edit encodersAB.h to comment out "#define ARBOTIX2" if using with an original arbotix
  * Edit ax12.h (in bioloid library) to comment out "#define ARBOTIX2" and select your other board type.

## PyPose Notes ##
To use PyPose with the ArbotiX2, you must install the ROS firmware (not the original PyPose sketch firmware, since that doesn't understand how to communicate with RX servos). Note that the ROS sketch now defaults to a baud rate of 115200, not 38400. Either edit the sketch before upload, or edit the line inside PyPose.py

## ROS Notes ##
The PC-side code from 0.4.1 release will work, but you need to use the updated firmware and libraries from above.

## Motors ##
You will need the latest robocontroller library release (0011) which includes updated

A Pololu motor driver can be plugged directly into the board, just install female headers in the empty socket at the top of the board (labeled with LPWM and RPWM)

Holes are provided for attaching standoffs to steady the motor driver -- the one near the XBEE header is a bit tight...

## Power ##
Prototypes shipped without a regulator installed. You may choose to:
  * power the logic aspects of the board from USB power and not install the regulator (keeping the height down!)
  * install the LM2940 regulator and capacitors included
  * install a Dimensions 5V 1A switching regulator -- which reduces heat dissipation and increases battery life.

Feedback about the option to get a board sans regulator is currently being sought.

RX and AX busses are powered separately, you need attach power to both terminal blocks if using RX (note: grounds ARE tied together).

## NUKE ##
To use exported NUKE code (or really, anything using the bioloid controller library) you will need to do the following. To initialize which servos are on the AX or RX bus, add the following code to your setup:
```
  delay(1000); 
  // do a search for devices on the RX bus, default to AX if not found
  int i;
  for(i=0;i<AX12_MAX_SERVOS;i++){
    dynamixel_bus_config[i] = 1;
    if(ax12GetRegister(i+1, AX_ID, 1) != (i+1)){
      dynamixel_bus_config[i] = 0;
    }
  }  
```
This would normally be added directly after the delay(1000) found in the NUKE exported sketch. And that is literally it! All other functions go about as usual.