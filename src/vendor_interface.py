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
# flake8: noqa: E501


import os
import sys
import toml
from vss_lib.vspec.model import Model
from vss_lib.vss_logging import logger
from invoke import run
from vss_lib.canbus import CANBusSimulator
from vss_lib.containers.podman import PodmanManager

CONFIG_PATH = '/etc/vss-lib/vss.config'

class VehicleSignalInterface:
    """
    Interface to interact with vehicle signal models for different vendors.

    Attributes:
        vendor (str): The vendor for which the interface is created.
        vspec_file (Optional[str]): Path to the VSS file for the vendor, default signals used if not provided.
        preference (Optional[dict]): User preferences for signal generation (e.g., ASIL, QM).
        attached_electronics (list): List of attached electronics vendors.
    """
    def __init__(self, vendor, vspec_file=None, preference=None, attached_electronics=None):
        """
        Initialize the VehicleSignalInterface and start the Podman container for the vendor.
        """
        logger.info(f"Initializing VehicleSignalInterface for vendor={vendor}, vspec_file={vspec_file}")

        self.vendor = vendor.lower()
        self.vspec_file = vspec_file or f"/usr/share/vss-lib/{vendor}.vspec"
        self.preference = preference
        self.attached_electronics = attached_electronics or []

        # Initialize CANBusSimulator
        self.canbus_simulator = CANBusSimulator()

        # Load the VSS model and assign it to self.model
        self.model = self.load_vspec_model(self.vspec_file)

        if not self.model:
            logger.error(f"Failed to load VSS model for {vendor}")
            raise ValueError(f"Model not found for {vendor}")

        # Start the Podman container to run the container_dbus_service
        self.dbus_manager = self.dbus_manager_service()
        self.joysticks_manager = self.joystick_manager_service()

        # Attach the electronics after the container is started
        self._attach_electronics()

    def dbus_manager_service(self):
        """
        Run the container_dbus_service inside a Podman container for the vendor.
        """
        try:
            # Create PodmanManager instance for the vendor
            podman_manager = PodmanManager(
                    vendor=self.vendor,
                    vspec_file=self.vspec_file,
                    containerfile="/usr/share/vss-lib/dbus-manager/ContainerFile"
            )

            # Build and run the Podman container
            podman_manager.build_container()
            podman_manager.run_container()

        except Exception as e:
            logger.error(f"Failed to start Podman container for {self.vendor}: {e}")
            raise RuntimeError(f"Podman container could not be started for {self.vendor}")

    def load_vspec_model(self, vspec_file):
        """
        Load the VSS model from the file and print the contents for debugging if errors occur.

        Args:
            vspec_file (str): The path to the VSS file.

        Returns:
            Model: The loaded VSS model object or None if loading fails.
        """
        try:
            model = Model.from_file(vspec_file)
            logger.info(f"Loaded VSS model from {vspec_file}")
            return model
        except Exception as e:
            logger.error(f"Failed to load VSS model from {vspec_file}: {e}")
            # Print the full path and contents of the VSS file for debugging
            if os.path.exists(vspec_file):
                logger.error(f"Full path of the VSS file: {os.path.abspath(vspec_file)}")
                with open(vspec_file, 'r') as file:
                    vss_content = file.read()
                    logger.error(f"VSS file content for {vspec_file}:\n{vss_content}")
            else:
                logger.error(f"VSS file {vspec_file} does not exist.")
            return None

    def _attach_electronics(self):
        """
        Attach electronics vendors to the running container.
        """
        if not self.attached_electronics:
            logger.info("No electronics to attach.")
            return
        logger.info(f"Attaching electronics to {self.vendor} container.")
        for electronics in self.attached_electronics:
            logger.info(f"Simulating CAN message for attached electronics: {electronics}")
            # Simulate encoding and decoding CAN messages for each attached electronic vendor
            self.simulate_can_message("attach_electronics", electronics)

    def get_signal_details(self, signal_name):
        """
        Retrieve the details of a specific signal.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: The details of the signal, or None if the signal is not found.
        """
        if not self.model:
            logger.error("VSS model not loaded.")
            return None
        return self.model.get_signal_details(signal_name)

    def validate_signal(self, signal_name, value):
        """
        Validate the value of a signal based on its range and datatype.

        Args:
            signal_name (str): The name of the signal.
            value: The value to validate.

        Returns:
            bool: True if the value is within the signal's valid range, else False.
        """
        signal_details = self.get_signal_details(signal_name)
        if signal_details:
            unit = signal_details.get('unit', None)
            min_value = signal_details.get('min', 0)
            max_value = signal_details.get('max', 100)

            if min_value <= value <= max_value:
                logger.info(f"Value {value} for signal '{signal_name}' is valid (min: {min_value}, max: {max_value}, unit: {unit if unit is not None else 'none'}).")
                # Simulate CAN message encoding and decoding on valid signals
                self.simulate_can_message(signal_name, value)
                return True
            else:
                logger.warning(f"Value {value} for signal '{signal_name}' is out of range (min: {min_value}, max: {max_value}, unit: {unit if unit is not None else 'none'}).")
                return False
        logger.error(f"Signal '{signal_name}' not found or invalid for validation.")
        return False

    def simulate_can_message(self, signal_name, value):
        """
        Simulate encoding and decoding a CAN message for the given signal and value.

        Args:
            signal_name (str): The name of the signal.
            value: The value to encode in the CAN message.
        """
        data = {"signal": signal_name, "value": value}
        encoded_message = self.canbus_simulator.encode_can_message(data)
        self.canbus_simulator.decode_can_message(encoded_message)

    def stop_podman_container(self):
        """
        Stop and remove the Podman container for the vendor.
        """
        try:
            # Create PodmanManager instance for the vendor
            podman_manager = PodmanManager(vendor=self.vendor, vspec_file=self.vspec_file, containerfile="/usr/share/vss-lib/dbus-manager/ContainerFile")

            # Stop the Podman container
            podman_manager.stop_container()

        except Exception as e:
            logger.error(f"Failed to stop Podman container for {self.vendor}: {e}")
            raise RuntimeError(f"Podman container could not be stopped for {self.vendor}")

    def joystick_manager_service(self):
        """
            Run the joystick Podman container.
        """
        try:
            # Create PodmanManager instance for joystick container
            podman_manager = PodmanManager(
                    vendor="joystick",
                    vspec_file=None,
                    containerfile="/usr/share/vss-lib/joysticks/ContainerFile"
            )

            # Build and run the joystick Podman container
            podman_manager.build_container()
            podman_manager.run_joystick_container()

        except Exception as e:
            logger.error(f"Failed to start joystick Podman container: {e}")
            raise RuntimeError(f"Joystick Podman container could not be started")

    def stop_joystick_container(self):
        """
        Stop and remove the joystick Podman container.
        """
        try:
            # Create PodmanManager instance for joystick container
            podman_manager = PodmanManager(vendor="joystick", vspec_file=None, containerfile="/usr/share/vss-lib/joysticks/ContainerFile")

            # Stop the joystick Podman container
            podman_manager.stop_container(container_name="joystick_vss_container")

        except Exception as e:
            logger.error(f"Failed to stop joystick Podman container: {e}")
            raise RuntimeError(f"Joystick Podman container could not be stopped")
