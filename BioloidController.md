# Introduction #
The BioloidController library is an easy way to interact with Bioloid servos. It consists of several files:
  * ax12.h & ax12.cpp - implement the low-level serial communications code for communicating with the Bioloid bus.
  * BioloidController.h & BioloidController.cpp - implement higher level functions, like loading a pose from FLASH memory, or manipulating poses.

This page will walk through the basics of using the BioloidController library. At times we will use **...** to truncate parts of the code in order to be more readable and focused. Full code examples can be found in the _sketches_ folder of the _arbotiX-software_ release.

# Getting Started #
AX-12 servos are different from regular hobby servos. They connect to a serial bus, and each has an ID number. Rather than receiving a PWM signal, we write to onboard memory locations through our serial protocol. For more information about AX-12 servos, see either this [tutorial on TRC](http://forums.trossenrobotics.com/tutorials/how-to-diy-128/controlling-ax-12-servos-3275/), or take a look at the [AX-12 datasheet](http://www.trossenrobotics.com/images/productdownloads/AX-12_Manual(English).pdf).

The lowest-level of the BioloidController library is composed of simple functions to read/write register locations on the AX-12. We have also provided a number of special definitions to make the most common operations a simple function call:
```
// need to include header files, you can do this in the Arduino IDE, by selecting Sketch|Import Library|Bioloid.
#include <ax12.h>
#include <BioloidController.h>

// we always need to create an instance of the bioloid control, usually with baud = 1Mbps.
BioloidController bioloid = BioloidController(1000000);

int i;
void setup(){
    i = 0;
}

void loop(){
    // set AX-12 servo with ID=1, to position i, where 0=<i<1024
    SetPosition(1,i);
    i = (i++)%1024;
}
```

Helper function macros include:
  * SetPosition(servo\_id, position) - set the position of a servo.
  * TorqueOn(servo\_id) - turns on the torque
  * Relax(servo\_id) - turns off the torque, allows hand-posing the servos.

However, you can access the full set of registers using:
  * ax12GetRegister(servo\_id, regstart, length) - read a register value back, _length_ should currently be either 1 or 2, _regstart_ should be the name/memory location of the register. All these definitions are included in ax12.h, such as AX\_GOAL\_POSITION\_L.
  * ax12SetRegister(servo\_id, regstart, data) - write the value of a single register within a servo. As above, _regstart_ should be the name/memory location of the register, data is the byte to be written.
  * ax12SetRegister2(servo\_id, regstart, data) - write the value of a 2-byte register.

# Using Poses #
Manipulating individual servos is nice, but when we have multi-servo legged robots, it can be slow and repetitive. A common solution is to use poses and to play the poses out to have the robot walk. If we have gathered our poses using PyPose, we will have exported a pose file that looks like:
```
#ifndef DROID_POSES
#define DROID_POSES

#include <avr/pgmspace.h>

PROGMEM prog_uint16_t liftLeft[] = {4, 612, 620, 450, 380};
PROGMEM prog_uint16_t plantRight[] = {4, 612, 620, 508, 516};
PROGMEM prog_uint16_t swingRight[] = {4, 612, 620, 710, 593};
PROGMEM prog_uint16_t swingLeft[] = {4, 413, 410, 450, 390};
PROGMEM prog_uint16_t plantLeft[] = {4, 418, 411, 503, 516};
PROGMEM prog_uint16_t liftRight[] = {4, 523, 520, 712, 592};

PROGMEM transition_t forward[] = {{0,7} ,{plantLeft,250} , ...

#endif
```
Where _droid_ was the name of our robot (PyPose automatically converts it to upper case during export), and liftLeft, plantRight, etc are the pose names. We will typically save our pose file as poses.h, in the directory where our sketch is located. This pose file is the example from our video of making the _walking droid_ work with an arbotiX. We'll discuss the transition sequence _(forward)_ later.

We can now load these poses from FLASH memory, and send them out to the servos using a bioloid-bus SyncWrite (which is much faster than setting the position of each servo individually).

<a href='Hidden comment: 
#include <ax12.h>
#include <BioloidController.h>
#include "poses.h"  // pose file generated from PyPose, currently in this sketch"s directory

// we always need to create an instance of the bioloid control, usually with baud = 1Mbps.
BioloidController bioloid = BioloidController(1000000);

// stand up
void setup(){
bioloid.loadPose(stand); // load a pose (named "stand") from FLASH into buffer
bioloid.writeSyncPose(); // write the buffer to the servos
}
void loop(){}The above example probably made our _walking droid_ jump up in the air, maybe even falling over, since our servos move so fast.
'></a>


# Interpolation Engine #
An important consideration is how fast should we move from one pose to another? If we move to fast, a walking robot will likely topple over. AX-12 servos are too fast to let them go directly to the new position, so if we want a gradual change, we will need to _interpolate_ between our current pose and our next pose. The BioloidController library allows this to be done very easily:

```
#include <ax12.h>
#include <BioloidController.h>
#include "poses.h"  // pose file generated from PyPose

BioloidController bioloid = BioloidController(1000000);

#define frames 6
int idx = 0;

// stand up slowly
void setup(){    
    delay(100);                    // recommended pause
    bioloid.loadPose(plantLeft);   // load the pose from FLASH, into the nextPose buffer
    bioloid.readPose();            // read in current servo positions to the curPose buffer
    bioloid.interpolateSetup(500); // setup for interpolation from current->next over 1/2 a second
    while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
        bioloid.interpolateStep();     // move servos, if necessary. 
        delay(3);
    }
}

void loop(){}
```
The interpolation engine is very simple. It writes a new frame out to the servos at about 30Hz. If your loop code gets really long, this could become problematic. Eventually, we will have an interpolation engine that is interrupt driven, so that the movement is more guaranteed to be smooth.

An item I did not discuss above, was bioloid.readPose(), this queries each servo, and loads their positions into the _curpose_ buffer. This is most useful for standing up gently, as shown above. bioloid.loadPose("pose\_name") always loads into the _nextpose_ buffer, and interpolation always happens from _curpose_ to _nextpose_. Note that is recommended to have a delay of at least 100ms after startup before a readPose(), otherwise the AX-12s may not be ready and legs may jitter.

# Walking with Sequences #
We could manually handle loading pose after pose and writing them out to the servos, or we can use a sequence. A sequence can be constructed in PyPose and is exported inside our pose file. Each sequence contains several transitions, each transition is a pose name and an interpolation time to use when transitioning to that pose.

```
#include <ax12.h>
#include <BioloidController.h>
#include "poses.h"

BioloidController bioloid = BioloidController(1000000);

void setup(){
    // stand up slowly
    delay(100);                    // recommended pause
    bioloid.loadPose(plantLeft);
    bioloid.readPose();
    bioloid.interpolateSetup(500);
    while(bioloid.interpolating > 0){
        bioloid.interpolateStep();
        delay(3);
    }
    
    // start our walking
    bioloid.playSeq(forward);
}

void loop(){
    bioloid.play();
}
```

We're using the same code to "stand" up, but then we call _playSeq()_ with the name of a sequence, in our case, _forward_ which will make the robot walk forward. _playSeq()_ is somewhat like _interpolateSetup()_, it just bootstraps our system. We need to call _play()_ just as we called _interpolateStep()_. Just like _bioloid.interpolating_, we have a variable that tells us when we're done, _bioloid.playing_.

# Walking with Fewer Poses #
Issy used only 3 poses for walking, one for normal standing position, and 2 for picking up each of our pairs of legs, but could do an unlimited number of step sizes. This was accomplished by basically parameterizing the length of the step. Eventually, PyPose and the BioloidController library will automatically support the creation of these parameterizations, but that is still in progress. Here is a sample of Issy's code, showing only the walking part in the loop:
```
// servo numbers
#define RIGHT_FRONT     5
#define LEFT_FRONT      6
#define RIGHT_REAR      11
#define LEFT_REAR       12
#define TILT_SERVO      13

...

void loop(){

    // we read in serial port data here, to control Issy via the XBEE radio....

    // update walking gait parameters
    if(bioloid.interpolating == 0){
        if((rstep != 0) || (lstep != 0)){    // do nothing if we are stopped
        if(walkMode == 0){
            bioloid.loadPose(walk0);
            bioloid.setNextPose(RIGHT_FRONT,bioloid.getNextPose(RIGHT_FRONT) - rstep);
            bioloid.setNextPose(LEFT_FRONT,bioloid.getNextPose(LEFT_FRONT) - lstep);
            bioloid.setNextPose(RIGHT_REAR,bioloid.getNextPose(RIGHT_REAR) + rstep);
            bioloid.setNextPose(LEFT_REAR,bioloid.getNextPose(LEFT_REAR) + lstep);
            walkMode = 1;
            bioloid.interpolateSetup(75);   
        }else if(walkMode == 1){
            bioloid.loadPose(walkend);
            bioloid.setNextPose(RIGHT_FRONT,bioloid.getCurPose(RIGHT_FRONT));
            bioloid.setNextPose(LEFT_FRONT,bioloid.getCurPose(LEFT_FRONT));
            bioloid.setNextPose(RIGHT_REAR,bioloid.getCurPose(RIGHT_REAR));
            bioloid.setNextPose(LEFT_REAR,bioloid.getCurPose(LEFT_REAR));
            walkMode = 2;
            bioloid.interpolateSetup(30);   
        }else if(walkMode == 2){
            bioloid.loadPose(walk1);
            bioloid.setNextPose(RIGHT_FRONT,bioloid.getNextPose(RIGHT_FRONT) + rstep);
            bioloid.setNextPose(LEFT_FRONT,bioloid.getNextPose(LEFT_FRONT) + lstep);
            bioloid.setNextPose(RIGHT_REAR,bioloid.getNextPose(RIGHT_REAR) - rstep);
            bioloid.setNextPose(LEFT_REAR,bioloid.getNextPose(LEFT_REAR) - lstep);
            walkMode = 3;
            bioloid.interpolateSetup(75);   
        }else{
            bioloid.loadPose(walkend);  
            bioloid.setNextPose(RIGHT_FRONT,bioloid.getCurPose(RIGHT_FRONT));
            bioloid.setNextPose(LEFT_FRONT,bioloid.getCurPose(LEFT_FRONT));
            bioloid.setNextPose(RIGHT_REAR,bioloid.getCurPose(RIGHT_REAR));
            bioloid.setNextPose(LEFT_REAR,bioloid.getCurPose(LEFT_REAR));
            walkMode = 0;
            bioloid.interpolateSetup(30);   
        }
        }else{
            // stopped! put feet down!
            bioloid.loadPose(walkend);  
            bioloid.setNextPose(RIGHT_FRONT,bioloid.getCurPose(RIGHT_FRONT));
            bioloid.setNextPose(LEFT_FRONT,bioloid.getCurPose(LEFT_FRONT));
            bioloid.setNextPose(RIGHT_REAR,bioloid.getCurPose(RIGHT_REAR));
            bioloid.setNextPose(LEFT_REAR,bioloid.getCurPose(LEFT_REAR));
            bioloid.interpolateSetup(30);   
        }   
    }
    
    // update joints
    bioloid.interpolateStep();
}
```

# Hacking #
You can change the speed of the interpolation engine, by changing the BIOLOID\_FRAME\_LENGTH in BioloidController.h.

If using more than 18 servos, you will need to change AX12\_MAX\_SERVOS in ax12.h to increase the size of the pose buffers. Alternatively, if memory is running tight, and you are using less than 18 servos, you can change this to reduce the size of the pose buffers.

Pose header files are very simple. We are using the program memory storage utilities of AVR-Libc in order to store the poses in the FLASH, rather than occupying RAM. Each pose is an array of integers, to put this array in program memory it is of type _PROGMEM prog\_uint16\_t_. The first element in the array is the servo count. The servo count can be 1-255, in the example below, Issy has 12 servos:
```
PROGMEM prog_uint16_t stand[ ] = {12,512,512,482,542,662,362,512,512,542,482,362,662}; 
```
Each number after the servo count is the position of the servo, starting with ID number 1. Positions are 0-1023, the same as what an AX-12 can actually take on.

_Note: The upper byte of the servo count is reserved for special values that may be used later to define special new types of poses_.
