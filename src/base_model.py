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
import os
from vss_lib.vss_logging import logger
from vss_lib.vspec.model import Model
from vss_lib.vendor_interface import VehicleSignalInterface
from vss_lib.vspec_parser import load_vspec_file

class BaseModel:
    """
    Base class for handling common signal operations across different vendors.
    """

    def __init__(self, vspec_file, vendor, preference, attached_electronics):
        """
        Initialize the model by loading the specified VSS file and setting up the vehicle interface.

        Args:
            vspec_file (str): The path to the VSS file.
            vendor (str): The name of the vehicle vendor.
            preference (str): The safety preference (ASIL, QM, etc.).
            attached_electronics (list): A list of attached electronics vendors.
        """
        # Ensure vspec_file is a full path
        if not os.path.isabs(vspec_file):
            vspec_file = f"/usr/share/vss-lib/{vspec_file}.vspec"

        self.vspec_file = vspec_file
        self.vspec_data = load_vspec_file(vspec_file)

        if self.vspec_data is None:
            raise AttributeError(f"Failed to load model from {vspec_file}")

        logger.info(f'Loaded VSS model from {vspec_file}')

        # Initialize VehicleSignalInterface for the vendor
        try:
            self.vehicle_signal_interface = VehicleSignalInterface(
                vendor=vendor, preference=preference, attached_electronics=attached_electronics
            )
            logger.info(f"VehicleSignalInterface initialized for {vendor}.")
        except Exception as e:
            logger.error(f"Failed to initialize VehicleSignalInterface for {vendor}: {e}")
            self.vehicle_signal_interface = None

        # Load available signals
        self.available_signals = self.load_available_signals()

    def load_available_signals(self):
        """
        Load and return the available signals from the model.

        Returns:
            list: A list of signal paths available in the model.
        """
        if self.vspec_data is None:
            raise AttributeError("BaseModel has no 'vspec_data' initialized.")

        return list(self.vspec_data.keys()) if self.vspec_data else []

    def attach_electronic(self, electronic_model):
        """
        Attach an electronics vendor to the car vendor.

        Args:
            electronic_model (object): The electronics model to attach.
        """
        self.attached_electronics.append(electronic_model)
        logger.info(f'Attached {electronic_model.__class__.__name__} to {self.__class__.__name__}')

    def get_signal_details(self, signal_name):
        """
        Get details of a signal by name.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: A dictionary containing signal details such as datatype,
                  unit, min, and max.
        """
        keys = signal_name.split(".")
        signal = self.vspec_data  # This is the loaded VSS model

        for key in keys:
            if isinstance(signal, dict):
                signal = signal.get(key)
            else:
                logger.error(f"Expected dictionary for signal path '{signal_name}', but got: {type(signal)}")
                return None

            if signal is None:
                logger.warning(f"Signal path '{signal_name}' not found.")
                return None

        # Ensure the signal is a dictionary and not an int or other type
        if not isinstance(signal, dict):
            logger.error(f"Expected signal details for '{signal_name}', but got: {type(signal)}")
            return None

        return {
            "datatype": signal.get('datatype'),
            "unit": signal.get('unit'),
            "min": signal.get('min'),
            "max": signal.get('max')
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
            if signal.get('min') <= value <= signal.get('max'):
                logger.info(f'Value {value} for signal "{signal_name}" is valid.')
                return True
            else:
                logger.warning(f'Value {value} for signal "{signal_name}" is out of range.')
                return False
        logger.error(f'Signal "{signal_name}" not found for validation.')
        return False
