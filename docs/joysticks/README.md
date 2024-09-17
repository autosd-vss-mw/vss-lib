# Documentation for Joystick

## PS5 Controller on Linux (Fedora 40)

When connecting a PS5 controller on Linux (Fedora 40), two input devices are created:

- `/dev/input/js0` - **Joystick Interface**
- `/dev/input/js1` - **Gamepad Interface**

### /dev/input/js0 - Joystick Interface

The joystick interface is an older, more basic system for handling input devices like game controllers. It predates the more flexible `evdev` (event device) system. While still in use, it's considered more limited in terms of functionality and support for modern controllers, especially compared to the gamepad interface.

### /dev/input/js1 - Gamepad Interface

The gamepad interface is a more standardized input interface used for handling game controllers in Linux. It abstracts some of the complexities of the controller, making it easier for applications, particularly games, to interpret input events such as button presses and axis movements.

