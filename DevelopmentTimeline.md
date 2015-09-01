# Revision History #

  * Release 0015 (10-1-2012, [r650](https://code.google.com/p/arbotix/source/detail?r=650)) - This release targets Arduino 1.0.1 and contains a number of bug fixes and improvments:
    * Arduino/Core:
      * All code compatible with Arduino 1.0.1
      * Upgraded boards.txt to use variants.
      * Analog pins are no longer reversed when using as digital pins, A0 is no D24, A1 is D25 ... A7 is D31.
    * PyPose:
      * Initial support for 12-bit servos.
      * Added Live Update mode which updates servos as sliders are dragged(enabled from config menu).
      * Added enable check boxes to relax individual joints.
      * .ppr is automatically added to the name of a pose file, if not included by user.
    * Library Changes/Improvements:
      * BioloidController:
        * Enabled pull up on serial rx pin, greatly reduces dropped packets on Bioloid bus.
        * New GetPosition(id) macro defined in ax12.h ([Issue #23](https://code.google.com/p/arbotix/issues/detail?id=#23))
        * Error levels are now defined in ax12.h
        * Added ax12GetLastError() to ax12.h to allow users to determine error level.
        * Variants are defined such that we no longer need to edit ax12.h to specify board type.
      * Motors2:
        * Merged in BigMotors library, usage is defined by board variant selected.
    * Distribution Change:
      * RoboControllerLib is now part of ArbotiX release.
      * PyPose will be released separately from ArbotiX.
    * Known Issues:
      * The screen may not resize correctly at times, it is recommended that you switch to a different tool and then back to the desired tool if the screen does not show some controls.
      * On some systems, ports may not be recognized, on Windows this especially means COMx where x > 20. It is recommended to use the serial command inside the Servo Terminal.
      * NUKE data saved with previous versions of PyPose may become garbled, in particular, check your servo ID mapping.

  * Release 0014 (2-16-2011, [r550](https://code.google.com/p/arbotix/source/detail?r=550)) - This release contains several updates and bug fixes.
    * Updated to new BioloidController library
    * FIXED: software commander walk/look joystick reversal.
    * AX-S1 driver macros ([Issue 10](https://code.google.com/p/arbotix/issues/detail?id=10))
    * Update internal core to 0019 spec.

  * Release 0013 (5-3-2010, [r481](https://code.google.com/p/arbotix/source/detail?r=481)) - This release contains numerous updates and bug fixes, as we roll out the RX-bridge, tested support for NUKE on hexapods, and a number of small tweaks to NUKE and related technologies. (May 2010)
    * FIXED: Keyboard Accelerator issues ([Issue 14](https://code.google.com/p/arbotix/issues/detail?id=14))
    * FIXED: Commander.py reversals from southpaw mods.
    * FIXED: Added LED blink routine previously removed from Commander Library to default NUKE sketch.
    * FIXED: Multiple issues with hexapods and NUKE, has now been fully tested for 3DOF Lizard hexapods.
    * BioloidController updates to allow RX servo control. ([Issue 19](https://code.google.com/p/arbotix/issues/detail?id=19))

  * Release 0012 Patch 1 (3-10-2010, [r457](https://code.google.com/p/arbotix/source/detail?r=457))
    * FIXED: Southpaw error in Commander library.
    * FIXED: Capture/Set pose gives port error when a pose is not selected. ([Issue #21](https://code.google.com/p/arbotix/issues/detail?id=#21))
    * Added programmers.txt
    * Beta of RX servo support

  * Release 0012 (2-21-2010, [r443](https://code.google.com/p/arbotix/source/detail?r=443))
    * FIXED: Issues with sequence export
    * Full NUKE support for Lizard IK
    * Re-ordered default servo mapping.
    * Relax servos at the beginning of neutral/limit captures
    * Move test drive button down near export
    * Messages after finishing neutral capture
    * Support for Arduino 0018

  * Release 0011 (1-3-10) (V1.1 Beta1)
    * First pass of NUKE IK interface (limits, neutrals, mapping, params)
    * Support for Lizard 3DOF, 4/6 legs
    * Released EncodersAB and Commander Libraries

  * Release 0010 (11-29-09, [r365](https://code.google.com/p/arbotix/source/detail?r=365)) (V1.0c)
    * FIXED: Issues with Delta-T under Pose Editor

  * Release 0009 (11-14-09, [r351](https://code.google.com/p/arbotix/source/detail?r=351)) (V1.0b)
    * Port drivers merged
    * Delta-T added to Pose Editor "set" command
    * Many libraries moved to [RoboControllerLib](http://robocontroller.googlecode.com)

  * Release 0008 (10-18-09, [r329](https://code.google.com/p/arbotix/source/detail?r=329)) (V1.0a)
    * FIXED: Port errors are actually now detected (arbotix.py pushes errors higher).
    * FIXED: Blank transition error.
    * FIXED: Timeout issues.
    * Port detection overhauled for MacOSX users.

  * Release 0007 (10/17/09) (rc1a)
    * FIXED: Save/load bug

  * Release 0007 (10/2/09) (rc1)
    * FIXED: Error messages in multiple places, cleaned up portions of code
    * FIXED: New project dialog.

  * Release 0006 (9/28/09) (Beta4a)
    * Updated libraries: pypose (for PyPose V0.97) was made much faster
    * PyPose Improvements: (V0.97)
      1. "robot" is now "project"
      1. Fixed various issues with dialogs and borders under Windows
      1. Reorganized tool structure
      1. Added first pass of Terminal tool
      1. Key shortcuts for pose operations
      1. Dialog added to change pose names
      1. Improved port management and error messages
      1. Selection of serial ports (rather than having to enter them)
      1. Includes all files we used to pull from Sanguino
    * Updated examples:
      1. droid (now includes droid.ppr)

  * Release 0005 (9/18/09) (Beta3b)
    * PyPose V0.93 - Live playback of sequences!

  * Release 0004 (9/16/09) (Beta3a)
    * Servo editors are now disabled until a pose is selected.

  * Release 0003 (9/15/09) (Beta3)
    * New libraries: Commander
    * PyPose improvements: (V0.91)
      1. Completely rewritten, using wxPython instead of TkInter
      1. Sequence creation
    * Bioloid library improvements:
      1. Sequence Engine
    * Updated examples: pypose

  * Release 0002 (8/27/09) (Beta2)
    * New libraries: Motors2, Srf05
    * Renamed libraries: sharpIR is now SharpIR, bioloid is now Bioloid
    * PyPose improvements: (V0.89)
      1. USBDynamixel driver _(note: currently not usable without editing code)_
    * New examples: issy

  * Release 0001 (8/8/09)
    * New libraries: bioloid, sharpIR
    * PyPose functionality: (V0.50)
      1. create robot files, capture poses
      1. export to AVR
      1. code and sketch to interact with arbotiX
    * New examples: droid, pypose

# Development Plans #
  * Add direct value entry box (checkable option under config)
  * Automatically highlight new pose when using "add".
  * Allow renaming of sequences.
  * Checkable option to torque on after capture?
  * Make NUKE correctly use a RH coordinate system.
  * Port Dialog Overhaul: Make the "open port" dialog easier to use. Add ability to switch driver characteristics.
  * Finish the Servo Terminal: Specifically, add the ability to fiddle with registers in a meaningful and easy fashion.
  * New Examples: a rover with closed loop feedback. Updated Issy (2DOF) using commander library. A biped example using poses and simple walk engine?
  * Nuke templates; 3DOF Mammal IK, 4/5/6 DOF Bipeds.
  * New Gaits: We currently have a number of Ripple, Amble, and Tripod Gaits. We'd like to add:
    1. Geometrically Stable Ripple. - _currently experimental_
    1. Possibly add support for planar tails to assist with stability.
  * Gait Template Structure: Currently, gaits are integrated into the templates, eventually we would like to support separate gait files.