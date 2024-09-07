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
from vss_lib.vspec.model import Model  # Correct import for Model
from vss_lib.vendor_interface import VehicleSignalInterface  # Ensure this is the correct import

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
        self.model = Model.from_file(self.vspec_file)  # Load the VSS model using Model class
        self.attached_electronics = []

        if self.model is None:
            raise AttributeError(f"Failed to load model from {vspec_file}")

        logger.info(f'Loaded VSS model from {vspec_file}')

        # Initialize VehicleSignalInterface for the vendor
        try:
            # Pass the model's vspec_data to VehicleSignalInterface
            self.vehicle_signal_interface = VehicleSignalInterface(
                vendor=vendor, vspec_data=self.model.vspec_data, preference=preference, electronics=attached_electronics
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
        if self.model is None:
            raise AttributeError("BaseModel has no 'model' initialized.")

        # Top-level keys in the VSS data represent the available signals
        return list(self.model.vspec_data.keys()) if self.model.vspec_data else []

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
        Retrieve details of a specific signal.

        Args:
            signal_name (str): The name of the signal to retrieve.

        Returns:
            dict: A dictionary containing signal details such as datatype,
                  unit, min, and max.
        """
        signal = self.model.find(f"Vehicle.{signal_name}")
        if signal:
            logger.info(f'Signal "{signal_name}" found with details.')
            return {
                "name": signal_name,
                "datatype": signal.get('datatype'),
                "unit": signal.get('unit'),
                "min": signal.get('min'),
                "max": signal.get('max'),
            }
        logger.warning(f'Signal "{signal_name}" not found.')
        return None

    def validate_signal(self, signal_name, value):
        """
        Validate the signal value for any model.

        Args:
            signal_name (str): The name of the signal.
            value: The value to validate.

        Returns:
            bool: True if the value is valid, else False.
        """
        signal = self.model.find(f"Vehicle.{signal_name}")
        if signal:
            if signal.get('min') <= value <= signal.get('max'):
                logger.info(f'Value {value} for signal "{signal_name}" is valid.')
                return True
            else:
                logger.warning(f'Value {value} for signal "{signal_name}" is out of range.')
                return False
        logger.error(f'Signal "{signal_name}" not found for validation.')
        return False
