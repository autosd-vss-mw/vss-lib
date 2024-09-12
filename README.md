# VSS-Lib: Vehicle Signal Specification Library

Vehicle Signal Specifications Python Library based on [COVESA (Connected Vehicle Systems Alliance)](https://covesa.global/) and [their specification](https://covesa.github.io/vehicle_signal_specification/).

VSS-Lib is a Python library and D-Bus service designed to interact with vehicle signals according to the Vehicle Signal Specification (VSS). It supports vendor-specific models and can emit random or real-time hardware signals to the D-Bus interface. The library also allows attaching electronics vendors to vehicle models.

## Features

- Emit random vehicle signals based on QM, ASIL, or UserPreference.
- Handle real-time hardware signals from baremetal devices.
- Attach electronics vendors to vehicle models for simulation.
- Monitor D-Bus for vehicle signal data.

## Requirements

- Python 3.10+
- `pydbus` for D-Bus interaction
- `pyyaml`
- `toml`
- `invoke`
- Systemd for managing the D-Bus service

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/vss-lib.git
cd vss-lib
```

### Step 2: Install Python Dependencies

Make sure you have Python 3.10+ installed. You can create a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install the Library

Install the library and the vss dbus demo service:

```bash
sudo pip install .
sudo systemctl daemon-reload
sudo systemctl enable vss-dbus.service
sudo systemctl start vss-dbus.service
sudo journalctl -u vss-dbus.service -f # Montior the deploy
sudo dbus-monitor --system "interface=com.vss_lib.VehicleSignals" # See all signals being sent
```

Start monitoring the Car Manufactors vendors and partners "speaking" the Vehicle Signal Specification (VSS) protocol on top of Fedora, CentOS.
```bash
sudo dbus-monitor --system "interface=com.vss_lib.VehicleSignals"

signal time=1725863086.478979 sender=:1.9701 -> destination=(null destination) serial=184 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Electronics.Bosch.ParkingSensorStatus.max"
   double 1.88863
signal time=1725863088.478907 sender=:1.9701 -> destination=(null destination) serial=185 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Speed.min"
   double 49.5526
signal time=1725863090.479247 sender=:1.9701 -> destination=(null destination) serial=186 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "BrakeFluidLevel.datatype"
   double 48.5111
signal time=1725863092.480390 sender=:1.9701 -> destination=(null destination) serial=187 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Electronics.Renesas.NavigationAccuracy.datatype"
   double 11.383
signal time=1725863094.479111 sender=:1.9701 -> destination=(null destination) serial=188 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Speed.unit"
   double 47.296
signal time=1725863096.479761 sender=:1.9701 -> destination=(null destination) serial=189 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Electronics.Renesas.NavigationAccuracy.unit"
   double 6.26474
```

(In a second terminal, see the containers created sending the ASIL and QM signals to the VSS DBUS manager demo using VSS specs):
```bash
vss-lib (main) $ sudo podman ps
[sudo] password for douglas:
CONTAINER ID  IMAGE                                COMMAND               CREATED             STATUS             PORTS       NAMES
9a5937f3a82f                                       /sbin/init            54 minutes ago      Up 54 minutes                  qm
b5659436d457  localhost/toyota_vss_image:latest    sh -c /usr/lib/py...  About a minute ago  Up About a minute              toyota_vss_container
e62bf9a0e121  localhost/bmw_vss_image:latest       sh -c /usr/lib/py...  About a minute ago  Up About a minute              bmw_vss_container
866ad65b24b9  localhost/ford_vss_image:latest      sh -c /usr/lib/py...  About a minute ago  Up About a minute              ford_vss_container
387283dc83e8  localhost/honda_vss_image:latest     sh -c /usr/lib/py...  About a minute ago  Up About a minute              honda_vss_container
1e7cbb90f017  localhost/jaguar_vss_image:latest    sh -c /usr/lib/py...  About a minute ago  Up About a minute              jaguar_vss_container
212b103ffd6a  localhost/mercedes_vss_image:latest  sh -c /usr/lib/py...  About a minute ago  Up About a minute              mercedes_vss_container
161f79e61eb7  localhost/volvo_vss_image:latest     sh -c /usr/lib/py...  About a minute ago  Up About a minute              volvo_vss_container
```

### Step 4: Install the Systemd Service (setup.py should do for you but in case you want to execute manual steps)

To enable and start the D-Bus service, follow these steps:

1. Copy the systemd service file to the appropriate directory:

```bash
sudo cp systemd/vss-dbus.service /etc/systemd/system/
```

2. Reload the systemd daemon:

```bash
sudo systemctl daemon-reload
```

3. Enable the D-Bus service to start at boot:

```bash
sudo systemctl enable vss-dbus.service
```

4. Start the service:

```bash
sudo systemctl start vss-dbus.service
```

5. Check the status of the service:

```bash
sudo systemctl status vss-dbus.service
```

### Step 5: Configure the VSS Paths

Ensure that the VSS configuration file `/etc/vss/vss.config` is correctly set up with paths to the vendor-specific VSS files.

Example configuration:

```ini
[global]
vspec_path=/usr/share/vss-lib/

[vehicle_toyota]
vspec_file=${vspec_path}toyota.vspec

[vehicle_bmw]
vspec_file=${vspec_path}bmw.vspec
```

## Monitoring Signals on the D-Bus Interface

Once the D-Bus service is running, you can monitor the random signals emitted by the VSS D-Bus service using `dbus-monitor`. This will show the signals in real-time as they are emitted.

Run the following command:

```bash
dbus-monitor "interface=com.vss_lib.VehicleSignals"
```

You should see random signals being emitted, similar to the following:

```bash
signal sender=:1.102 -> dest=(null destination) serial=44 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=EmitHardwareSignal
   string "Speed"
   double 80.0
```

## Sending Hardware Signals

If you want to send hardware signals from a Python script, you can use the D-Bus client included in this project:

```python
from pydbus import SystemBus

def send_hardware_signal(signal_name, value):
    bus = SystemBus()
    vss_service = bus.get("com.vss_lib.VehicleSignals")
    vss_service.EmitHardwareSignal(signal_name, value)

# Example: Sending a speed signal with a value of 80
send_hardware_signal("Speed", 80)
```

## Uninstalling

To stop and disable the D-Bus service:

```bash
sudo systemctl stop vss-dbus.service
sudo systemctl disable vss-dbus.service
```

To uninstall the library and clean up:

```bash
pip uninstall vss-lib
sudo rm /etc/systemd/system/vss-dbus.service
sudo rm /etc/vss/vss.config
```

## Contributing

Feel free to open an issue or submit a pull request if you'd like to contribute to the project.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.
