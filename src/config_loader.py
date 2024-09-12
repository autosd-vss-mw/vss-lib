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
import toml
import yaml

CONFIG_PATH = '/etc/vss-lib/vss.config'


def get_vspec_file(vendor):
    """
    Get the VSS file path for the given vendor or electronics component.

    Args:
        vendor (str): The name of the vendor or electronics component.

    Returns:
        str: The path to the VSS file, or None if not found.
    """
    config_path = '/etc/vss-lib/vss.config'
    vspec_file = None

    # Load the TOML configuration file
    try:
        with open(config_path, 'r') as config_file:
            config = toml.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return None
    except toml.TomlDecodeError as e:
        print(f"Error decoding TOML file: {e}")
        return None

    # First, check for electronics section in the config file
    electronics_section = f"electronics_{vendor.lower()}"
    vehicle_section = f"vehicle_{vendor.lower()}"

    if electronics_section in config:
        vspec_file = config[electronics_section].get("vspec_file")
    elif vehicle_section in config:
        vspec_file = config[vehicle_section].get("vspec_file")
    else:
        print(f"Configuration section not found for vendor: {vendor}")
        return None

    if vspec_file and os.path.exists(vspec_file):
        return vspec_file
    else:
        print(f"VSS file not found for vendor: {vendor}")
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
