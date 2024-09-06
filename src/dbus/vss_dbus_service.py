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
import time
import os
import threading
from pydbus.generic import signal
from vss_lib.vendor_interface import VehicleSignalInterface
from vss_lib.vss_logging import logger
import configparser

class VehicleSignalService:
    """
    D-Bus Service to send random vehicle signals or hardware-based signals.

    This service supports both simulated signals (QM, ASIL) and real-time hardware signals.
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

    def __init__(self, config_path='/etc/vss/vss.config'):
        self.vsi = None  # This will be initialized based on the configuration
        self.hardware_signals = {}  # Dictionary to store hardware signals
        self.load_configuration(config_path)

    def load_configuration(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        if 'vehicle_toyota' in config:
            vendor = config.get('vehicle_toyota', 'vendor')
            vspec_file = config.get('vehicle_toyota', 'vspec_file')
            preference = config.get('vehicle_toyota', 'preference')
            attached_electronics = config.get('vehicle_toyota', 'attach_electronics').split(',')

            # Pass the values to initialize VehicleSignalInterface
            self.vsi = VehicleSignalInterface(vendor, vspec_file, preference, attached_electronics)
            logger.info(f"Initialized VehicleSignalInterface for {vendor}")
 
    def load_available_signals(self):
        """
        Load all available signals from the VSS model.

        Returns:
            list: A list of all signal names available in the VSS model.
        """
        if self.vsi is None:
            logger.warning("VehicleSignalInterface not initialized")
            return []

        # Assuming the VehicleSignalInterface or model can list available signals
        available_signals = []
        for signal in self.vsi.model.signals:
            available_signals.append(signal.name)

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
            value = random.uniform(signal_details['min'], signal_details['max'])
            logger.info(f"Generated random value {value} for signal {signal_name}")
            return signal_name, value
        return None, None

    def EmitSignal(self, signal_name, value):
        """
        Emit the signal over D-Bus.
        """
        logger.info(f"Emitting signal {signal_name} with value {value}")
        self.SignalEmitted(signal_name, value)

    def StartSignalEmission(self):
        """
        Emit random signals at regular intervals.
        """
        while True:
            signal_name, value = self.GetRandomSignal()
            if signal_name:
                self.EmitSignal(signal_name, value)
            time.sleep(2)

    def EmitHardwareSignal(self, signal_name, value):
        """
        Allow users to manually send signals from hardware to the D-Bus interface.
        """
        self.hardware_signals[signal_name] = value
        logger.info(f"Received hardware signal {signal_name} with value {value}")
        self.EmitSignal(signal_name, value)


if __name__ == "__main__":
    service = VehicleSignalService()

    # Start the emission thread
    signal_thread = threading.Thread(target=service.StartSignalEmission)
    signal_thread.daemon = True
    signal_thread.start()

    # Setup the D-Bus service
    bus = SystemBus()
    bus.publish(
        "com.vss_lib.VehicleSignals",
        service
    )

    # Setup the main loop
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        logger.info("Service interrupted by user.")
