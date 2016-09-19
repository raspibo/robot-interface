# robot-interface

An interface for controlling robots via browser.

There are two python scripts:

- "painter.py" is just for testing purposes, it displays mouse or joystick/joypad movements in a pygame screen
- "servo.py" needs a Raspberry Pi of any model, it starts a servoblaster daemon (part of PiBits by richardghirst https://github.com/richardghirst/PiBits ), reads a joystick or joypad (not a mouse, for the moment) and writes the value to the servo device file; it accepts one argument, the signal pin for the servo in p1pin format (default is 22)

This interface is tested on Firefox 48.0, it should work on webkit browsers as well but at the moment it fails.

To exit press CTRL-C.

