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


class MercedesModel(BaseModel):
    """
    Mercedes-specific signal model. This class extends the BaseModel to include
    signals specific to Mercedes vehicles.
    """

    def __init__(self, preference=None, attached_electronics=None):
        """
        Initialize the Mercedes model by loading the VSS file path from the configuration.
        Args:
            preference (Optional[dict]): User preferences that may influence signal generation.
            attached_electronics (Optional[list]): List of attached electronics, such as ECUs.
        """
        vendor = "mercedes"  # Set the required vendor argument
        vspec_file = get_vspec_file(vendor)
        if vspec_file:
            # Pass vendor, vspec_file, preference, and attached_electronics to BaseModel's constructor
            super().__init__(vendor, vspec_file, preference, attached_electronics)
            self.attached_electronics = attached_electronics or []
        else:
            raise ValueError("Mercedes VSS file path not found in the configuration.")
