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


import yaml


def load_vspec_file(vspec_file_path):
    """
    Load the VSS file for the vehicle signals.

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


def get_signal(model, path):
    """
    Find and return a signal by its path.

    Args:
        model (Model): The VSS model.
        path (str): The signal path within the model.

    Returns:
        Signal: The signal object if found, else None.
    """
    return model.find(path)
