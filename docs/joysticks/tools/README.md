## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [Supported Controllers](#supported-controllers)
    - [Sony DualShock 4](#sony-dualshock-4)
    - [Sony DualSense](#sony-dualsense)
    - [Sony PS VR Aim Controller](#sony-ps-vr-aim-controller)
    - [PNX Flight Simulator PC Game Controller](#pnx-flight-simulator-pc-game-controller)
    - [Nintendo Switch Pro Controller](#nintendo-switch-pro-controller)
    - [Stadia Controller (Google)](#stadia-controller-google)
    - [Xbox One Elite 2 Controller](#xbox-one-elite-2-controller)
    - [HORI Racing Wheel Apex](#hori-racing-wheel-apex)
    - [Valve Software Wired Controller (Steam Controller)](#valve-software-wired-controller-steam-controller)

## Overview

This tool detects connected PS4, PS5 (DualSense), PS VR Aim controllers, Nintendo Switch Pro Controller, Stadia Controller, PNX Flight Simulator PC Game Controller, Xbox One Elite 2 Controller, HORI Racing Wheel Apex, or Valve Software Wired Controller (Steam Controller), tracks their inputs, and manages the special features of the DualSense controller (PS5). It is built using Pygame for general input handling and pydualsense for controlling the advanced features of the PS5 DualSense controller.

The tool also checks if the `vss-dbus` service is running, which could cause conflicts with the joystick device, and exits if the service is active.

## Features

- **PS4/PS5/PS VR Aim Controller Input Logging**: Logs the button, axis, and D-pad (hat) inputs of a connected PS4, PS5, or PS VR Aim controller.
- **Motor Vibration Control**: Uses Button 10 (Options button) to toggle motor vibration on and off for PS4 and PS5 controllers. The vibration will continue until Button 10 is pressed again.
- **DualSense Controller Features**: Leverages the pydualsense library to manage advanced features of the PS5 DualSense controller, including motor control.
- **PS VR Aim Controller Support**: Logs inputs from the PS VR Aim Controller. Vibration is currently not supported for this device.
- **PNX Flight Simulator PC Game Controller Support**: Logs inputs from the PNX Flight Simulator PC Game Controller.
- **Nintendo Switch Pro Controller Support**: Logs inputs from the Nintendo Switch Pro Controller.
- **Stadia Controller Support**: Logs inputs from the Stadia Controller by Google.
- **Xbox One Elite 2 Controller Support**: Logs inputs from the Xbox One Elite 2 Controller, supporting general input logging.
- **HORI Racing Wheel Apex Support**: Logs inputs from the HORI Racing Wheel Apex, recognized as a gamepad.
- **Valve Software Wired Controller (Steam Controller) Support**: Logs inputs from the Steam Controller. Vibration support is not yet implemented.
- **vss-dbus Conflict Detection**: Ensures the tool does not run if the `vss-dbus` service is active to avoid device conflicts.
- **Graceful Exit**: The tool handles `Ctrl + C` signals to exit gracefully, stopping any active vibration and releasing resources.

## Prerequisites

- **Pygame**: For general joystick handling.
- **pydualsense**: For advanced DualSense controller features (PS5).

To install the dependencies:

```bash
pip install pygame pydualsense
```

## Usage

Ensure that the `vss-dbus` service is stopped before running the tool:

```bash
sudo systemctl stop vss-dbus
```

Run the tool with root permissions:

```bash
sudo ./gaming-controllers
pygame 2.6.0 (SDL 2.28.4, Python 3.12.5)
Hello from the pygame community. https://www.pygame.org/contribute.html
Detected controller: Stadia Controller
Controller has 13 buttons, 6 axes, 1 hats (D-pad)
Axis 2 moved to -1.000
Button 0 pressed
Button 0 released
```

## Supported Controllers

### Sony DualShock 4

When a Sony DualShock 4 (CUH-ZCT2x) controller with ID `054c:09cc` is connected, it is recognized as a "Wireless Controller" by the system.

#### `lsusb` Output:

```
Bus 003 Device 009: ID 054c:09cc Sony Corp. DualShock 4 [CUH-ZCT2x]
```

#### `dmesg` Output:

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

### Sony DualSense

Logs and supports advanced features of the PS5 DualSense controller, including motor vibration control.

#### `lsusb` Output:

```
Bus 003 Device 011: ID 054c:0ce6 Sony Corp. DualSense Controller
```

#### `dmesg` Output:

```
[85532.752523] usb 3-1: new full-speed USB device number 11 using xhci_hcd
[85532.879869] usb 3-1: New USB device found, idVendor=054c, idProduct=0ce6, bcdDevice= 1.01
[85532.879873] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[85532.879874] usb 3-1: Product: DualSense Wireless Controller
[85532.879875] usb 3-1: Manufacturer: Sony Interactive Entertainment
[85532.882135] playstation 0003:054C:0CE6.0007: hidraw0: USB HID v1.11 Gamepad [Sony Interactive Entertainment DualSense Wireless Controller] on usb-0000:00:14.0-1/input3
[85532.935872] input: Sony Interactive Entertainment DualSense Wireless Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.3/0003:054C:0CE6.0007/input/input43
```

### Sony PS VR Aim Controller

Logs input but does not support motor vibration.

#### `lsusb` Output:

```
Bus 003 Device 021: ID 054c:0bb2 Sony Corp. PS VR Aim Controller
[100945.936852] usb 3-1: Manufacturer: Sony Interactive Entertainment
```

#### `dmesg` Output:

```
[100945.809572] usb 3-1: new full-speed USB device number 23 using xhci_hcd
[100945.936846] usb 3-1: New USB device found, idVendor=054c, idProduct=0bb2, bcdDevice= 1.00
[100945.936850] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[100945.936851] usb 3-1: Product: PS VR Aim Controller
[100945.936852] usb 3-1: Manufacturer: Sony Interactive Entertainment
[100945.939224] input: Sony Interactive Entertainment PS VR Aim Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/0003:054C:0BB2.0014/input

/input70
[100945.939475] hid-generic 0003:054C:0BB2.0014: input,hidraw0: USB HID v1.11 Gamepad [Sony Interactive Entertainment PS VR Aim Controller] on usb-0000:00:14.0-1/input0
```

### PNX Flight Simulator PC Game Controller

Recognized as a USB HID joystick, logs all inputs from the PNX Flight Simulator PC Game Controller.

#### `lsusb` Output:

```
Bus 003 Device 037: ID 11ff:3331 PNX Flight Simulator PC Game Controller
```

#### `dmesg` Output:

```
[178965.304471] usb 3-1: new low-speed USB device number 37 using xhci_hcd
[178965.434131] usb 3-1: New USB device found, idVendor=11ff, idProduct=3331, bcdDevice= 1.07
[178965.434135] usb 3-1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[178965.434136] usb 3-1: Product: PC Game Controller
[178965.438067] gembird 0003:11FF:3331.0030: fixing Gembird JPD-DualForce 2 report descriptor.
[178965.438139] input: PC Game Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/0003:11FF:3331.0030/input/input79
[178965.438291] gembird 0003:11FF:3331.0030: input,hidraw0: USB HID v1.10 Joystick [PC Game Controller] on usb-0000:00:14.0-1/input0
```

### Nintendo Switch Pro Controller

Logs input from the Nintendo Switch Pro Controller.

#### `lsusb` Output:

```
Bus 003 Device 038: ID 057e:2009 Nintendo Co., Ltd. Switch Pro Controller
```

#### `dmesg` Output:

```
[180762.873610] usb 3-1: new full-speed USB device number 38 using xhci_hcd
[180763.001848] usb 3-1: New USB device found, idVendor=057e, idProduct=2009, bcdDevice= 2.10
[180763.001852] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[180763.001853] usb 3-1: Product: Pro Controller
[180763.001854] usb 3-1: Manufacturer: Nintendo Co., Ltd.
[180763.001855] usb 3-1: SerialNumber: 000000000001
[180763.004299] input: Nintendo Co., Ltd. Pro Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/0003:057E:2009.0031/input/input80
[180763.004575] hid-generic 0003:057E:2009.0031: input,hidraw0: USB HID v1.11 Joystick [Nintendo Co., Ltd. Pro Controller] on usb-0000:00:14.0-1/input0
[180763.607894] nintendo 0003:057E:2009.0031: hidraw0: USB HID v81.11 Joystick [Nintendo Co., Ltd. Pro Controller] on usb-0000:00:14.0-1/input0
[180764.466024] nintendo 0003:057E:2009.0031: controller MAC = 98:41:5C:35:6A:DC
[180764.498042] nintendo 0003:057E:2009.0031: using factory cal for left stick
```

### Stadia Controller (Google)

Logs input from the Stadia Controller by Google.

#### `lsusb` Output:

```
Bus 003 Device 039: ID 18d1:9400 Google Stadia Controller
```

#### `dmesg` Output:

```
[182836.887828] usb 3-1: new high-speed USB device number 39 using xhci_hcd
[182837.014560] usb 3-1: New USB device found, idVendor=18d1, idProduct=9400, bcdDevice= 1.00
[182837.014565] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[182837.014566] usb 3-1: Product: Stadia Controller
[182837.014566] usb 3-1: Manufacturer: Google Inc.
[182837.014567] usb 3-1: SerialNumber: 9A170YCAC5WNTR
[182837.017203] input: Google Inc. Stadia Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.1/0003:18D1:9400.0032/input/input83
[182837.017466] hid-generic 0003:18D1:9400.0032: input,hidraw0: USB HID v1.11 Gamepad [Google Inc. Stadia Controller] on usb-0000:00:14.0-1/input1
[182837.014565] usb 3-1: Product: Stadia Controller
[182837.014566] usb 3-1: Manufacturer: Google Inc.
```

### Xbox One Elite 2 Controller

Logs input from the Xbox One Elite 2 controller.

#### `lsusb` Output:

```
Bus 003 Device 041: ID 045e:0b00 Microsoft Corp. Xbox One Elite 2 Controller
[183717.391820] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[183717.391821] usb 3-1: Product: Controller
[183717.391821] usb 3-1: Manufacturer: Microsoft
[183717.391822] usb 3-1: SerialNumber: 3032363330313133383232313433
[183717.393388] input: Microsoft X-Box One Elite 2 pad as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/input/input86
```

#### `dmesg` Output:

```
[183717.264044] usb 3-1: new full-speed USB device number 41 using xhci_hcd
[183717.391816] usb 3-1: New USB device found, idVendor=045e, idProduct=0b00, bcdDevice= 4.07
[183717.391820] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[183717.391821] usb 3-1: Product: Controller
[183717.391821] usb 3-1: Manufacturer: Microsoft
[183717.391822] usb 3-1: SerialNumber: 3032363330313133383232313433
[183717.393388] input: Microsoft X-Box One Elite 2 pad as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/input/input86
```

### HORI Racing Wheel Apex

Recognized as a USB HID gamepad, logs inputs from the HORI Racing Wheel Apex.

#### `lsusb` Output:

```
Bus 003 Device 048: ID 0f0d:0156 HORI CO.,LTD. HORI Racing Wheel Apex
```

#### `dmesg` Output:

```
[186875.331973] usb 3-1: new full-speed USB device number 48 using xhci_hcd
[186875.461355] usb 3-1: New USB device found, idVendor=0f0d, idProduct=0156, bcdDevice= 1.15
[186875.461359] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[186875.461360] usb 3-1: Product: HORI Racing Wheel Apex
[186875.461361] usb 3-1: Manufacturer: HORI CO.,LTD.
[186875.463351] input: HORI CO.,LTD. HORI Racing Wheel Apex as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/0
003:0F0D:0156.0039/input/input93
[186875.463647] hid-generic 0003:0F0D:0156.0039: input,hiddev96,hidraw0: USB HID v1.11 Gamepad [HORI CO.,LTD. HORI
 Racing Wheel Apex] on usb-0000:00:14.0-1/input0

```

### Valve Software Wired Controller (Steam Controller)

The Valve Software Wired Controller (Steam Controller) is supported, and its inputs are logged. While vibration support is not currently implemented, basic input tracking (button and analog stick) is available.

#### `lsusb` Output:

```
Bus 003 Device 050: ID 28de:1102 Valve Software Wired Controller
```

#### `dmesg` Output:

```
[188467.414066] usb 3-1: new full-speed USB device number 50 using xhci_hcd
[188467.541684] usb 3-1: New USB device found, idVendor=28de, idProduct=1102, bcdDevice= 1.00
[188467.541689] usb 3-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[188467.541690] usb 3-1: Product: Wired Controller
[188467.541691] usb 3-1: Manufacturer: Valve Software
[188467.543753] input: Valve Software Wired Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.0/0003:28DE:1102.003E/input/input99
[188467.595514] hid-steam 0003:28DE:1102.003E: input,hidraw0: USB HID v1.11 Keyboard [Valve Software Wired Controller] on usb-0000:00:14.0-1/input0
[188467.596074] input: Valve Software Wired Controller as /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1:1.1/0003:28DE:1102.003F/input/input100
```
