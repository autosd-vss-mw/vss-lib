# PS4, PS5, and PS VR Aim Joystick Controller Logger

## Overview

This tool detects connected PS4, PS5, and PS VR Aim controllers, tracks their inputs, and manages the special features of the DualSense controller (PS5), such as motor vibration. It is built using Pygame for general input handling and pydualsense for controlling the advanced features of the PS5 DualSense controller.

The tool also checks if the `vss-dbus` service is running, which could cause conflicts with the joystick device, and exits if the service is active.

## Features

- **PS4/PS5/PS VR Aim Controller Input Logging**: Logs the button, axis, and D-pad (hat) inputs of a connected PS4, PS5, or PS VR Aim controller.
- **Motor Vibration Control**: Uses Button 10 (Options button) to toggle motor vibration on and off for PS4 and PS5 controllers. The vibration will continue until Button 10 is pressed again.
- **DualSense Controller Features**: Leverages the pydualsense library to manage advanced features of the PS5 DualSense controller, including motor control.
- **PS VR Aim Controller Support**: Logs inputs from the PS VR Aim Controller. Vibration is currently not supported for this device.
- **vss-dbus Conflict Detection**: Ensures the tool does not run if the `vss-dbus` service is active to avoid device conflicts.
- **Graceful Exit**: The tool handles `Ctrl + C` signals to exit gracefully, stopping any active vibration and releasing resources.

## Prerequisites

- **Pygame**: For general joystick handling.
- **pydualsense**: For advanced DualSense controller features (PS5).

## Supported Controllers

- PS4 (DualShock 4)
- PS5 (DualSense)
- PS VR Aim Controller (input logging, no vibration)
```

## Prerequisites

- **Pygame**: For general joystick handling.
- **pydualsense**: For advanced DualSense controller features.

To install the dependencies:
```bash
pip install pygame pydualsense
```

## Usage

Ensure that the `vss-dbus` service is stopped before running the tool:
```bash
sudo systemctl stop vss-dbus
```

The tool will detect a connected PS4 or PS5 controller, log its inputs, and allow motor vibration control via Button 10 (Options button).
```bash
sudo ./ps-controllers-pygame
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

## Sony DualShock 4 Connection Information

When a Sony DualShock 4 (CUH-ZCT2x) controller with ID `054c:09cc` is connected, it is recognized as a "Wireless Controller" by the system. Below is an example of the connection process logged by the system:

### `lsusb` Output:

```
Bus 003 Device 009: ID 054c:09cc Sony Corp. DualShock 4 [CUH-ZCT2x]
```

### `dmesg` Output:

```
[73828.815810] usb 3-1: new full-speed USB device number 9 using xhci_hcd
[73828.943692] usb 3-1: New USB device found, idVendor=054c, idProduct=09cc, bcdDevice= 1.00
[73828.943696] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[73828.943697] usb 3-1: Product: Wireless Controller
[73828.943698] usb 3-1: Manufacturer: Sony Interactive Entertainment
[73828.951819] playstation 0003:054C:09CC.0006: hidraw0: USB HID v1.11 Gamepad [Sony Interactive Entertainment Wireless Controller] on usb-0000:00:14.0-1/input3
[73829.004491] input: Sony Interactive Entertainment Wireless Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.3/0003:054C:09CC.0006/input/input38
[73829.004751] input: Sony Interactive Entertainment Wireless Controller Motion Sensors as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.3/0003:054C:09CC.0006/input/input39
[73829.004778] input: Sony Interactive Entertainment Wireless Controller Touchpad as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.3/0003:054C:09CC.0006/input/input40
[73829.004874] playstation 0003:054C:09CC.0006: Registered DualShock4 controller hw_version=0x0000a40c fw_version=0x0000904d
```

The controller is recognized successfully and registered with motion sensors and a touchpad, using the playstation driver to manage inputs.

## Sony PS VR Aim Controller Connection Information

When a Sony PS VR Aim Controller with ID `054c:0bb2` is connected, it is recognized by the system. Below is an example of the connection process logged by the system:

### `lsusb` Output:

```
Bus 003 Device 021: ID 054c:0bb2 Sony Corp. PS VR Aim Controller
```

### `dmesg` Output:

```
[100945.809572] usb 3-1: new full-speed USB device number 23 using xhci_hcd
[100945.936846] usb 3-1: New USB device found, idVendor=054c, idProduct=0bb2, bcdDevice= 1.00
[100945.936850] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[100945.936851] usb 3-1: Product: PS VR Aim Controller
[100945.936852] usb 3-1: Manufacturer: Sony Interactive Entertainment
[100945.939224] input: Sony Interactive Entertainment PS VR Aim Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/0003:054C:0BB2.0014/input/input70
[100945.939475] hid-generic 0003:054C:0BB2.0014: input,hidraw0: USB HID v1.11 Gamepad [Sony Interactive Entertainment PS VR Aim Controller] on usb-0000:00:14.0-1/input0
```

The controller is recognized successfully by the system as a USB HID gamepad, and the input device is registered with the hid-generic driver.
