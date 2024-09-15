# Documentation for Joystick
# -----------------------------
# PS5 controller used when implemented the joystick interface, when connected on
# Linux (Fedora 40) it created /dev/input/js0 and /dev/input/js1 where:
#
# /dev/input/js0 = Joystick interface
# ------------------------------------------
# The joystick interface in Linux is an older and more basic interface for handling
# input devices like game controllers. It predates the more flexible
# evdev (event device) system, and while it is still in use, it's often considered
# more limited in terms of functionality and support for modern controllers compared
# to the gamepad interface.
#
# /dev/input/js1 = Gamepad interface
# ------------------------------------------
# The gamepad interface is a more standardized input interface that is used
# for handling game controllers on systems like Linux. It represents the
# controller in a way that abstracts some of the complexities, making it
# easier for applications, particularly games, to understand and interact
# with the controller's input events (such as button presses and axis movements).
