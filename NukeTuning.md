# Overview of the IK Solution and Gait Engine #

NUKE generates a full inverse kinematics solution and a gait engine for your robot. However, you may want to tune it by hand. Before you can tune a system though, you'll need to know how it works.

NUKE exports 4 files:
  * _nuke.h_ - header file for IK and gait engine
  * _nuke.cpp_ - contains the IK engine
  * _gaits.h_ - contains the gait engine
  * _something.pde_ - your sketch, this is where you'll put the robot's task-related code.

The main loop of your program, in _something.pde_ will look like this:
```
void loop(){
  // put your task code here
  // make sure it doesn't take too long to execute each cycle

  if(bioloid.interpolating == 0){
    // last step is done, do the next
    doIK();
    bioloid.interpolateSetup(tranTime);
  }
  bioloid.interpolateStep();
```

Your code will interact with the gait engine using several global variables, which can be set at any time, from anywhere in your code:
  * _Xspeed_ - the forward speed to walk at, in millimeters/second. Forward is positive.
  * _Yspeed_ - the sideways speed to walk at, in millimeters/second. Right is positive.
  * _Rspeed_ - the speed to turn at, in radians/second.

The body IK engine also relies on several other variables:
  * _bodyPosX_, _bodyPosY_ - offset of the center of body in the air, in millimeters.
  * _bodyRotX_, _bodyRotY_, _bodyRotZ_ - rotation of body about axis, in radians.

The most important function is clearly _doIK()_ which ties everything from NUKE together. _doIK()_ generates the IK solution for each leg's servos, taking into account the default positions (created in _setupIK()_), gait requests, and the bodyIK parameters such as body yaw or pitch. You shouldn't need to alter the _doIK()_, _bodyIK()_ or _legIK()_. Most of the optimization that end users can do is in _setupIK()_ and the gait generators.

# Basic Gaits #
Basic gaits are cyclic. We can see that as a robot moves forward, it moves it's legs in some cyclic order. NUKE uses a gait generator function to create these movements. By passing in the leg ID and the _step_ variable, the gait generator creates a set of offsets (X,Y,Z,rotation about Z) for the given leg at that step. The _step_ variable counts from 0 to the number of steps in the currently selected gait -- this number is known as the _stepsInCycle_. For each cycle, every leg will move the desired distance (which is controlled by the speed variables).

A basic gait generator looks like this:
```
ik_req_t DefaultGaitGen(int leg){
 // TODO: add code here!!!!
}
```

By default, NUKE generates _continuous gaits_. Continuous gaits are such that the body moves in the desired direction at a continuous rate. A discontinuous gait is one that moves the body only when all feet are on the ground. When a gait is not stable enough, especially over terrain, creating a discontinuous gait may be of help.

# Gaits Included #
A number of gaits are included, which can be selected using the _SelectGait()_ function: (NOTE: SOME GAITS NOT YET IN BETA)

  * _Ripple_ gaits move only one leg at a time:
    * RIPPLE - the simplest, default gait. 8 steps per cycle (12 for a hexapod). Each leg is raised, and lowered, in order.
    * SMOOTH\_RIPPLE - similar but with as twice as many steps as a RIPPLE. Makes better foot paths.
    * FAST\_RIPPLE - 4 steps per cycle, 6 for a hexapod. As a leg lowers, another is already rising. Can be faster than RIPPLE, but may be very jerky or unsteady.
  * _Amble_ gaits move two alternate legs at a time:
    * AMBLE - 4 steps per cycle, each pair of legs is raised and moved forward in one step, then dropped in the next step.
    * SMOOTH\_AMBLE - similar to an AMBLE, but with twice as many steps per cycle.
  * _Tripod_ gaits move three legs at a time (For hexapods only):
    * TRIPOD - 4 steps per cycle, like an AMBLE, but using 3 legs in a group.
  * _Geometric_ gaits are the most stable for quadrupeds, but may be slower (For quadrupeds only):
    * RIPPLE\_GEO - a geometrically confined ripple, 8 steps per cycle. (Not included in  PyPose/NUKE V1.1)

# Default Stance, Length of Stride as an Optimization Factor #
NUKE computes the _Configuration Space_ of your robot's legs. The configuration space is the region of space where the legs can actually touch without any servo going out of range. From this, it can find what the default stance should be in order to maximize stride.

For most quadrupeds and hexapods, this is a good starting place. However, you may find yourself wanting to tune the default stance. This can be done by editing the _setupIK()_ function. _setupIK_ sets the position of the servos when the robot first starts up, and this position is what we add gait requests and body rotation requests to when we compute the final leg positions at each step in our cycle.

Future versions of NUKE may also allow optimizations for maximal stability rather than stride length, however, at this point you would have to hand optimize for this, a first step would be the use of a Geometrically Stable gait.

# Geometric Stability #
<font color='#FF0000'> This section describes a feature available only in NUKE V1.2 and above</font>
NUKE can generate a geometrically stable gait, that is, the _Center-of-Gravity_ of the robot is always within the _Support Polygon_ created by the feet that remain on the ground.

The _Stability Margin_ is the shortest length from the COG to the support polygon as projected along the direction of gravity. What the heck does that mean? On an incline, your stability margin is less than on flat ground. Frequently, the stability margin may be difficult or impossible to determine, and so approximations are often used.

<font color='#FF0000'> TODO: add images of stability margin/etc </font>

# Creating New Gait Generators #
There are two steps to creating a new gait. First, you must create a new gait generator and possibly a new gait setup, and then add the gait to the SelectGait function.

<font color='#FF0000'> TODO: add discussion of creating Gait Generators and Setup functions, the use of tranTime, etc</font>

After creating your new gait, you need to add the ability to select the gait. To add a new gait to your SelectGait function, you'll typically add to the end of the long set of _if/else_ statements:
```
    ...
    }else if(GaitType == MY_NEW_GAIT){
        gaitSetup = &MyGaitSetup;
        gaitGen = &MyGaitGenerator;
        gaitLegNo[RIGHT_FRONT] = 0;
        gaitLegNo[LEFT_FRONT] = 2;
        gaitLegNo[RIGHT_REAR] = 4;
        gaitLegNo[LEFT_REAR] = 6;
        pushSteps = 6;
        stepsInCycle = 8;
    }
```
Your code must define:
  * _stepsInCycle_ - the number of steps in a complete cycle
  * _pushSteps_ - the number of steps in a cycle where the leg is on the ground, and thus pushing in the desired direction. From a theoretical standpoint, the duty factor of each leg (time on the ground) = pushSteps/stepsInCycle.
  * _gaitLegNo_ - defines the order in which legs are moved. How this is used depends on the gait generator and gait setup functions selected.
  * _gaitSetup_ - the gait setup function to call at the beginning of each cycle. _DefaultGaitSetup_ is a default, and empty, gait setup function.
  * _gaitGen_ - the gait generator to call for each leg. _DefaultGaitGen_ is a default gait generator, which all non-geometric built-in gaits are currently using.

Optionally, you may also define:
  * _tranTime_- the time, in milliseconds, taken to do the interpolation from one position to the next. In a steady-period gait, the time taken for a cycle is simply tranTime\*stepsInCycle.
  * _cycleTime_ - the time, in seconds, taken to complete a cycle. Will normally be set to (stepsInCycle\*tranTime)/1000.0. However, if you are changing tranTime inside your custom gait generator, you need to set cycleTime explicitly!

# Other Hacking #

<font color='#FF0000'> TODO: add what values mean, out of range issues, etc </font>

Under development in V2.0/SVN-LATEST is a new gait file format. Gait files (.gait) contain the following:

```
REQUIRES: leg 4 6
REQUIRES: ik lizard3 mammal3
GAIT:MY_GAIT_NAME 
gaitGen = &NewGaitGen;
gaitSetup = &DefaultGaitSetup;
gaitLegNo[RIGHT_FRONT] = 0;
gaitLegNo[LEFT_MIDDLE] = 0;
gaitLegNo[RIGHT_REAR] = 0;
gaitLegNo[LEFT_REAR] = 2;
gaitLegNo[LEFT_FRONT] = 2;
gaitLegNo[RIGHT_REAR] = 2;
pushSteps = 2;	
stepsInCycle = 4;     
GENERATOR: NewGaitGen, This is a new gait generator
if( MOVING ){ 
  ...
}
SETUP: NewGaitSetup, This is a new setup function
...
GLOBAL: variableIneed
```

The first line is a requirements statement, that this gait is only for 4 or 6 legged robots. The second line is an additional statement that this gait is only to be used for the mammal3 or lizard3 IK specifications.

Where MY\_GAIT\_NAME would be something like AMBLE\_SMOOTH. This is followed by the actual gait generation code. We then have defined a GENERATOR, which has a name, and a description (which will be used as a comment), followed by the body of the function.

This file format will be used to generate the _gaits.h_ file automatically.