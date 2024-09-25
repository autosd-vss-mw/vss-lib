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


from vss_lib.base_model import BaseModel
from vss_lib.config_loader import get_vspec_file
from vss_lib.vss_logging import logger


class BoschModel(BaseModel):
    """
    Bosch-specific electronics model. This class extends the BaseModel to include
    signals specific to Bosch electronics components.
    """

    def __init__(self, preference=None, attached_electronics=None):
        """
        Initialize the Bosch model by loading the VSS file path from the configuration.

        Args:
            preference (Optional[dict]): User preferences that may influence signal generation.
            attached_electronics (Optional[list]): List of attached electronics, such as sensors or ECUs.
        """
        vendor = "bosch"  # Set the required vendor argument
        vspec_file = get_vspec_file(vendor)

        if vspec_file:
            # Initialize the BaseModel with vendor, VSS file, preference, and attached electronics
            super().__init__(vspec_file, vendor, preference, attached_electronics)
            logger.info(f"BoschModel initialized with VSS file: {vspec_file}")
        else:
            logger.error("Bosch VSS file path not found in the configuration.")
            raise ValueError("Bosch VSS file path not found in the configuration.")

    def attach_electronic(self, electronic_model):
        """
        Attach an electronics component to the Bosch model.
        """
        logger.info(f"Attached {electronic_model.__class__.__name__} to BoschModel")
        if not hasattr(self, 'attached_electronics'):
            self.attached_electronics = []
        self.attached_electronics.append(electronic_model)
