There are several other libraries that have been developed specifically for the arbotiX:
  * [Motors2](OtherLibraries#Motors2.md) - for using the onboard motor drivers

Additionally, the arbotiX can use the libraries found in the [robocontroller](http://robocontroller.googlecode.com) package.
  * Commander - library for communicating with a handheld arbotiX Commander, or a PC.
  * Encoders - for using the onboard encoder headers, this is actually two libraries: EncodersAB, for traditional quadrature encoders that output A&B signals, and EncodersCD for encoders that give out _clock_ and _direction_ signals.
  * SharpIR - for reading distance using any of the family of Sharp IR ranging sensors.
  * Srf05 - for reading distance using an Srf05 sonar sensors.
  * Srf08 - for reading distance using an Srf02 or Srf08 sonar sensor.

And of course, the stock Arduino libraries such as _Serial_ and _Servo_ can be used. See some hints [here](OtherLibraries#Arduino_Hints.md).

# Motors2 #
This library implements a dual motor driver using Timer2, it can be used to control the onboard motor driver on the arbotiX. It has several functions:

```
void left(int pwm) - set the left motor speed.
void right(int pwm) - set the right motor speed.
void set(int lpwm, int rpwm) - set the left and right motor speeds at the same time.
```

Motor speeds are between -255 and 255. -255 is full reverse, 0 is stopped, and 255 is full speed forward.

```
#include <Motors2.h>

Motors2 drive = Motors2();

void setup(){
    drive.set(-255,-255); // drive backwards at full speed 
    delay(1000);

    drive.set(0,0); // stop
    delay(1000);

    drive.set(100,100); // drive forward at half speed
    delay(1000);

    drive.left(0); // stop the left motor, turn in place
    delay(500);    
    drive.right(50); // cut right motor speed in half
    delay(500)
    drive.right(0); // and stop
}

void loop(){
    
}
```

# Arduino Hints #
The default _Serial_ library that comes with Arduino environment will work with either the FTDI cable or the XBEE radio on the arbotiX _(remember, don't connect both the FTDI and the XBEE at the same time)._ We suggest using 38400 as the baud rate, since all of our demos use that.

The default _Servos_ library is shipped with the Sanguino installation. Please note that it is not the same servo library found in the newer Arduino 0017 release, it is still the 2-servo hardware timer version. This servo library can be used to control the two servo headers found on the arbotiX.