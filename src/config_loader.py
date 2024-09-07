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
import yaml

CONFIG_PATH = '/etc/vss-lib/vss.config'


def get_vspec_file(vendor):
    """
    Load and parse the VSS YAML file for the given vendor.

    Args:
        vendor (str): The vendor name (e.g., 'toyota', 'bmw').

    Returns:
        dict: Parsed VSS YAML data.
    """
    # Load the configuration file (still using toml or configparser to get paths)
    config = toml.load(CONFIG_PATH)
    
    vendor_section = f"vehicle_{vendor}"

    if vendor_section in config:
        vspec_file_path = config[vendor_section].get('vspec_file', None)
        if vspec_file_path:
            return load_vspec_file(vspec_file_path)
    return None


def load_vspec_file(vspec_file_path):
    """
    Load and parse the VSS file for the vehicle signals from a YAML file.

    Args:
        vspec_file_path (str): Path to the VSS file.

    Returns:
        dict: Parsed VSS data.
    """
    try:
        with open(vspec_file_path, 'r') as file:
            vspec_data = yaml.safe_load(file)
            return vspec_data
    except FileNotFoundError:
        print(f"VSS file not found: {vspec_file_path}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    return None
