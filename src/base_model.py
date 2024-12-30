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

from vss_lib.vss_logging import logger
from vss_lib.vendor_interface import VehicleSignalInterface
from vss_lib.uds import UDSHandler
from vss_lib.vspec_parser import load_vspec_file
from config_loader import get_vspec_file, load_config
from vss_lib.canbus import CANTransport
from vss_lib.uprotocol import UProtocol


class BaseModel:
    """
    Base class for handling common signal operations across different vendors.
    """

    def __init__(self, vendor, preference, attached_electronics):
        """
        Initialize the model by loading the VSS file for the specified vendor
        and setting up the vehicle interface.
        """
        self.config = self.load_config()
        self.vendor = vendor
        self.preference = preference
        self.attached_electronics = attached_electronics or []

        # Load the VSS file path for the vendor
        vspec_file = get_vspec_file(vendor)
        if not vspec_file:
            raise FileNotFoundError(f"VSS file for vendor '{vendor}' not found.")

        # Load VSS data
        self.vspec_data = load_vspec_file(vspec_file)
        if not self.vspec_data:
            raise AttributeError(f"Failed to load model from {vspec_file}")
        logger.info(f"Loaded VSS model from {vspec_file}")

        # Initialize VehicleSignalInterface
        try:
            self.vehicle_signal_interface = VehicleSignalInterface(
                vendor=vendor, preference=preference, attached_electronics=self.attached_electronics
            )
            logger.info(f"VehicleSignalInterface initialized for {vendor}.")
        except Exception as e:
            logger.error(f"Failed to initialize VehicleSignalInterface for {vendor}: {e}")
            self.vehicle_signal_interface = None

        # Load available signals
        self.available_signals = self.load_available_signals()

        # Initialize UDSHandler
        try:
            self.uds_handler = UDSHandler(
                transport_layer=self.setup_transport(), config=self.config.get("uds", {})
            )
            logger.info("UDSHandler initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize UDSHandler: {e}")
            self.uds_handler = None

    def load_config(self):
        """
        Fetch configuration from the config_loader.

        Returns:
            dict: The loaded configuration as a dictionary.
        """
        return load_config("/etc/vss-config")

    def setup_transport(self):
        """
        Setup the transport layer for UDS communication.

        Returns:
            object: Transport object (CANTransport, UProtocol, etc.)
        """
        transport_type = self.config.get("transport_type", "CAN").lower()
        if transport_type == "can":
            return CANTransport()
        elif transport_type == "uprotocol":
            return UProtocol()
        else:
            raise ValueError(f"Unsupported transport type: {transport_type}")

    def load_available_signals(self):
        """
        Load and return the available signals from the model.

        Returns:
            list: A list of signal paths available in the model.
        """
        if not self.vspec_data:
            raise AttributeError("BaseModel has no 'vspec_data' initialized.")
        return list(self.vspec_data.keys())

    def attach_electronic(self, electronic_model):
        """
        Attach an electronics vendor to the car vendor.

        Args:
            electronic_model (object): The electronics model to attach.
        """
        self.attached_electronics.append(electronic_model)
        logger.info(f"Attached {electronic_model.__class__.__name__} to {self.__class__.__name__}")

    def get_signal_details(self, signal_name):
        """
        Get details of a signal by name.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: A dictionary containing signal details such as datatype, unit, min, and max.
        """
        keys = signal_name.split(".")
        signal = self.vspec_data

        for key in keys:
            if isinstance(signal, dict):
                signal = signal.get(key)
            else:
                logger.error(f"Expected dictionary for signal path '{signal_name}', got: {type(signal)}")
                return None
            if signal is None:
                logger.warning(f"Signal path '{signal_name}' not found.")
                return None

        if not isinstance(signal, dict):
            logger.error(f"Expected signal details for '{signal_name}', got: {type(signal)}")
            return None

        return {
            "datatype": signal.get("datatype"),
            "unit": signal.get("unit"),
            "min": signal.get("min"),
            "max": signal.get("max"),
        }

    def validate_signal(self, signal_name, value):
        """
        Validate the signal value for any model.

        Args:
            signal_name (str): The name of the signal.
            value: The value to validate.

        Returns:
            bool: True if the value is valid, else False.
        """
        signal = self.get_signal_details(signal_name)
        if signal:
            if signal.get("min") <= value <= signal.get("max"):
                logger.info(f"Value {value} for signal '{signal_name}' is valid.")
                return True
            logger.warning(f"Value {value} for signal '{signal_name}' is out of range.")
            return False
        logger.error(f"Signal '{signal_name}' not found for validation.")
        return False
