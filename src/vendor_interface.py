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

class VehicleSignalInterface:
    """
    Interface to interact with vehicle signal models for different vendors.

    Attributes:
        vendor (str): The vendor for which the interface is created.
        vendor_model (object): The specific vendor's model handler.
        electronics (list): List of attached electronics vendors.
    """

    def __init__(self, vendor, electronics=None):
        """
        Initializes the VehicleSignalInterface based on the provided vendor and electronics.

        Args:
            vendor (str): The vehicle vendor (e.g., 'toyota', 'bmw').
            electronics (list, optional): List of electronics vendors to attach (e.g., ['bosch', 'renesas']).

        Raises:
            ValueError: If the vendor is not supported.
        """
        self.vendor = vendor.lower()
        self.vendor_model = None
        self.electronics = electronics or []

        # Assign the appropriate vendor model based on the input
        self._initialize_vendor_model()

        # Attach electronics vendors if provided
        self._attach_electronics()

        logger.info(f"VehicleSignalInterface initialized for vendor {self.vendor}")

    def _initialize_vendor_model(self):
        """
        Initialize the vendor model based on the vendor provided.
        """
        if self.vendor == "toyota":
            from vss_lib.vendor.toyota import ToyotaModel
            self.vendor_model = ToyotaModel()
        elif self.vendor == "bmw":
            from vss_lib.vendor.bmw import BMWModel
            self.vendor_model = BMWModel()
        elif self.vendor == "ford":
            from vss_lib.vendor.ford import FordModel
            self.vendor_model = FordModel()
        elif self.vendor == "mercedes":
            from vss_lib.vendor.mercedes import MercedesModel
            self.vendor_model = MercedesModel()
        elif self.vendor == "honda":
            from vss_lib.vendor.honda import HondaModel
            self.vendor_model = HondaModel()
        elif self.vendor == "volvo":
            from vss_lib.vendor.volvo import VolvoModel
            self.vendor_model = VolvoModel()
        elif self.vendor == "jaguar":
            from vss_lib.vendor.jaguar import JaguarModel
            self.vendor_model = JaguarModel()
        else:
            raise ValueError(f"Unsupported vendor: {self.vendor}")

    def _attach_electronics(self):
        """
        Attach electronics vendors to the vendor model.
        """
        if not self.electronics:
            return

        from vss_lib.vendor.electronics import bosch, renesas

        for electronic in self.electronics:
            try:
                if electronic.lower() == "bosch":
                    self.vendor_model.attach_electronic(bosch.BoschModel())
                elif electronic.lower() == "renesas":
                    self.vendor_model.attach_electronic(renesas.RenesasModel())
                else:
                    logger.warning(f"Unsupported electronic vendor: {electronic}. Skipping.")
            except Exception as e:
                logger.error(f"Error attaching electronic {electronic}: {e}")

    def get_signal_details(self, signal_name):
        """
        Get details of a signal by name.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: A dictionary containing signal details such as datatype,
                  unit, min, and max.
        """
        return self.vendor_model.get_signal_details(signal_name)

    def validate_signal(self, signal_name, value):
        """
        Validate the value of a signal based on its range.

        Args:
            signal_name (str): The name of the signal.
            value: The value to validate.

        Returns:
            bool: True if the value is within the signal's valid range, else False.
        """
        return self.vendor_model.validate_signal(signal_name, value)
