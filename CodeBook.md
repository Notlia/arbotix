

# Voltage Monitoring #
It's a good idea to monitor the battery voltage, especially with LiPO chemistries. NOTE: Monitoring of batteries in software is no replacement for hardware-based monitoring.

A simple check at startup can be implemented, which stops the robot from starting up. This piece of code could be inserted into the beginning of the setup() function, and will stop the robot from starting up if the voltage is less than 10V. It requires that an AX-12 servo is connected, and set to ID 1:
```
  // wait, then check the voltage (LiPO safety)
  delay (1000);
  float voltage = (ax12GetRegister (1, AX_PRESENT_VOLTAGE, 1)) / 10.0;
  Serial.print ("System Voltage: ");
  Serial.print (voltage);
  Serial.println (" volts.");
  if (voltage < 10.0)
    while(1);
```

A more complete example can be found in [sketches/VoltTempMonitoring.pde](http://code.google.com/p/arbotix/source/browse/trunk/sketches/VoltTempMonitoring.pde)

# Tips From The InterbotiX Kits #
When using a Commander, you can easily change between gaits and speeds. This same code could be used on other robots:
```
// above setup/loop:
int multiplier;

#define RIPPLE_SPEED    1
#define AMBLE_SPEED     3
#define TRIPOD_SPEED    4
#define TOP_SPEED       9   //8-9 for ax-12, 10ish for ax-18F

// end of setup():
multiplier = RIPPLE_SPEED;

// loop() function:
void loop(){
  // take commands
  if(command.ReadMsgs() > 0){
    digitalWrite(0,HIGH-digitalRead(0));
    // select gaits
    if(command.buttons&BUT_R1){ gaitSelect(RIPPLE_SMOOTH); multiplier=RIPPLE_SPEED;}
    if(command.buttons&BUT_R2){ gaitSelect(AMBLE_SMOOTH); multiplier=AMBLE_SPEED;}
    if(command.buttons&BUT_R3){ gaitSelect(RIPPLE); multiplier=RIPPLE_SPEED;}
    if(command.buttons&BUT_L4){ gaitSelect(AMBLE); multiplier=AMBLE_SPEED;}
    if(command.buttons&BUT_L5){ gaitSelect(TRIPOD); multiplier=TRIPOD_SPEED;}
    if(command.buttons&BUT_L6){ gaitSelect(TRIPOD); multiplier=TOP_SPEED;}
    // set movement speed
    Xspeed = multiplier*(command.walkV);
    if((command.buttons&BUT_LT) > 0)
      Yspeed = multiplier*(command.walkH/2);
    else
      Rspeed = -(command.walkH)*multiplier/300.0;
    bodyRotY = (((float)command.lookV))/250.0;
    if((command.buttons&BUT_RT) > 0)
      bodyRotX = ((float)command.lookH)/250.0;
    else
      bodyRotZ = ((float)command.lookH)/250.0;
  }
  
  // if our previous interpolation is complete, recompute the IK
  if(bioloid.interpolating == 0){
    doIK();
    bioloid.interpolateSetup(tranTime);
  }
  
  // update joints
  bioloid.interpolateStep();
}
```

# Other Code Examples #
  * [Control a robot with plain text over XBEE](http://forums.trossenrobotics.com/showpost.php?p=44430&postcount=20)
  * [Using poses with the Commander library](http://forums.trossenrobotics.com/showpost.php?p=44687&postcount=54)