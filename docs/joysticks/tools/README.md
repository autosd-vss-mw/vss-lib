# PS5 Joystick Controller Logger

## Overview

This tool detects a connected PS5 controller, tracks its inputs, and manages the special features of the DualSense controller, such as motor vibration. It is built using Pygame for general input handling and pydualsense for controlling the advanced features of the DualSense controller.

The tool checks if the `vss-dbus` service is running, which could cause conflicts with the joystick device, and exits if the service is active. 

## Features

- **PS5 Controller Input Logging**: Logs the button, axis, and D-pad (hat) inputs of a connected PS5 controller.
- **Motor Vibration Control**: Uses Button 10 (Options button) to toggle motor vibration on and off.
- **DualSense Controller Features**: Leverages the pydualsense library to manage the advanced features of the DualSense controller, including motor control.
- **vss-dbus Conflict Detection**: Ensures the tool does not run if the `vss-dbus` service is active to avoid device conflicts.

## Prerequisites

- **Pygame**: For general joystick handling.
- **pydualsense**: For advanced DualSense controller features.
  
To install the dependencies:
```bash
pip install pygame pydualsense
```

To run and start seeing the controller codes for the commands you execute.... very useful for testing joysticks in Linux for car simulations. Use CTRL-C to force exit. 
```bash
$ sudo ./ps5-controller-pygame
pygame 2.6.0 (SDL 2.28.4, Python 3.12.5)
Hello from the pygame community. https://www.pygame.org/contribute.html
error: XDG_RUNTIME_DIR is invalid or not set in the environment.
Detected controller: Sony Interactive Entertainment Wireless Controller
['DpadDown', 'DpadLeft', 'DpadRight', 'DpadUp', 'L1', 'L2', 'L2Btn', 'L3', 'LX', 'LY', 'R1', 'R2', 'R2Btn', 'R3', 'RX', 'RY', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'accelerometer', 'circle', 'cross', 'gyro', 'micBtn', 'options', 'ps', 'setDPadState', 'share', 'square', 'touch1', 'touch2', 'touchBtn', 'touchFinger1', 'touchFinger2', 'touchLeft', 'touchRight', 'trackPadTouch0', 'trackPadTouch1', 'triangle']
Controller has 13 buttons, 6 axes, 1 hats (D-pad)
Axis 2 moved to -1.000
Axis 5 moved to -1.000
Button 0 pressed
Button 0 released
Button 3 pressed
Button 3 released
```
