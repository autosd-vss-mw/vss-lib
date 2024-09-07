#!/usr/bin/env python3
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pydbus import SystemBus
from gi.repository import GLib
import random
import toml
import time
from pydbus.generic import signal
from vss_lib.vendor_interface import VehicleSignalInterface
from vss_lib.vss_logging import logger

class VehicleSignalService:
    """
    D-Bus Service to send random vehicle signals or hardware-based signals.
    """
    dbus = """
    <node>
      <interface name='com.vss_lib.VehicleSignals'>
        <method name='EmitHardwareSignal'>
          <arg type='s' name='signal_name' direction='in'/>
          <arg type='d' name='value' direction='in'/>
        </method>
        <signal name='SignalEmitted'>
          <arg type='s' name='signal_name'/>
          <arg type='d' name='value'/>
        </signal>
      </interface>
    </node>
    """

    SignalEmitted = signal()  # Declare the D-Bus signal

    def __init__(self, config_path='/etc/vss-lib/vss.config'):
        self.vsi = None  # This will be initialized based on the configuration
        self.hardware_signals = {}  # Dictionary to store hardware signals
        self.load_configuration(config_path)

    def load_configuration(self, config_path):
        # Load the TOML configuration file
        config = toml.load(config_path)

        vendor_count = 0  # Track the number of vendors loaded

        # Interpolate the `vspec_path` defined in the global section
        global_config = config.get('global', {})
        vspec_path = global_config.get('vspec_path', '')

        # Iterate through all sections in the config file
        for section, values in config.items():
            if section.startswith('vehicle_'):
                vendor = values.get('vendor')
                vspec_file = values.get('vspec_file')

                # Perform manual interpolation for vspec_file if it uses the ${vspec_path} macro
                if '${vspec_path}' in vspec_file:
                    vspec_file = vspec_file.replace('${vspec_path}', vspec_path)

                preference = values.get('preference', None)
                attached_electronics = values.get('attach_electronics', [])

                # Log to verify correct file paths
                logger.info(f"Loading configuration for {vendor} from VSS file: {vspec_file}")

                # Initialize the VehicleSignalInterface
                self.vsi = VehicleSignalInterface(vendor, vspec_file, preference, attached_electronics)
                logger.info(f"Initialized VehicleSignalInterface for {vendor}")

                vendor_count += 1

        # If no vendors were loaded, log a warning message
        if vendor_count == 0:
            logger.warning("No vendors found in the configuration. No VehicleSignalInterface instances loaded.")

    def load_available_signals(self):
        """
        Load all available signals from the VSS model.

        Returns:
           list: A list of all signal names available in the VSS model.
        """
        if self.vsi is None:
            logger.warning("VehicleSignalInterface not initialized")
            return []

        # Assuming self.vsi.model.signals is a dictionary where keys are signal names
        available_signals = list(self.vsi.model.signals.keys())
        logger.info(f"Loaded available signals: {available_signals}")
        return available_signals

    def GetRandomSignal(self):
        """
        Generates and returns a random signal with a random value.
        Ensures that the signal is part of the VSS specification.
        """
        if self.vsi is None:
            logger.warning("VehicleSignalInterface not initialized")
            return None, None

        # Load available signals from the VSS model
        available_signals = self.load_available_signals()

        if not available_signals:
            logger.warning("No available signals to emit.")
            return None, None

        # Select a random signal from the available signals
        signal_name = random.choice(available_signals)

        # Check if the signal is defined in the VSS model
        signal_details = self.vsi.get_signal_details(signal_name)

        if signal_details:
            min_value = signal_details.get('min')
            max_value = signal_details.get('max')

            # Ensure min and max values are not None
            if min_value is None or max_value is None:
                logger.error(f"Signal {signal_name} is missing min or max value. Cannot generate random value.")
                return None, None

            try:
                value = random.uniform(min_value, max_value)
                logger.info(f"Generated random value {value} for signal {signal_name}")
                return signal_name, value
            except TypeError as e:
                logger.error(f"Error generating random value for signal {signal_name}: {e}")
                return None, None
        else:
            logger.warning(f"Signal details for {signal_name} not found.")
            return None, None

    def EmitSignal(self, signal_name, value):
        """
        Emit the signal over D-Bus.
        """
        logger.info(f"Emitting signal {signal_name} with value {value}")
        self.SignalEmitted(signal_name, value)

    def StartSignalEmission(self):
        """
        Emit random signals at regular intervals using GLib.timeout_add_seconds.
        """
        def emit_callback():
            signal_name, value = self.GetRandomSignal()
            if signal_name:
                self.EmitSignal(signal_name, value)
            return True  # Returning True ensures the function is called again

        GLib.timeout_add_seconds(2, emit_callback)

    def EmitHardwareSignal(self, signal_name, value):
        """
        Allow users to manually send signals from hardware to the D-Bus interface.
        """
        self.hardware_signals[signal_name] = value
        logger.info(f"Received hardware signal {signal_name} with value {value}")
        self.EmitSignal(signal_name, value)


if __name__ == "__main__":
    service = VehicleSignalService()

    # Setup the D-Bus service
    bus = SystemBus()
    bus.publish(
        "com.vss_lib.VehicleSignals",
        service
    )

    # Start the signal emission within the GLib main loop
    service.StartSignalEmission()

    # Setup the main loop
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        logger.info("Service interrupted by user.")
