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

import toml

CONFIG_PATH = '/etc/vss-lib/vss.config'


def get_vspec_file(vendor):
    """
    Load the VSS file path from the configuration file for the given vendor.

    Args:
        vendor (str): The vendor name (e.g., 'toyota', 'bmw').

    Returns:
        str: Path to the VSS file.
    """
    # Load the TOML configuration
    config = toml.load(CONFIG_PATH)

    vendor_section = f"vehicle_{vendor}"

    # Check if the vendor section exists in the configuration
    if vendor_section in config:
        return config[vendor_section].get('vspec_file', None)
    
    return None
