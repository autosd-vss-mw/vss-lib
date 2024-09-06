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
# vspec/model.py

import json
from vss_lib.vss_logging import logger

class Model:
    """
    Class for managing vehicle signals from VSS files.
    """

    def __init__(self, vspec_data):
        """
        Initialize the model with the loaded VSS data.

        Args:
            vspec_data (dict): The parsed VSS data.
        """
        self.vspec_data = vspec_data

    @classmethod
    def from_file(cls, vspec_file):
        """
        Load a VSS file and create a Model instance.

        Args:
            vspec_file (str): The path to the VSS file.

        Returns:
            Model: An instance of the Model class.
        """
        try:
            with open(vspec_file, 'r') as file:
                data = json.load(file)
                logger.info(f'Successfully loaded VSS file: {vspec_file}')
                return cls(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f'Error loading VSS file {vspec_file}: {e}')
            return None

    def find(self, path):
        """
        Find and return a signal by its path.

        Args:
            path (str): The signal path within the model.

        Returns:
            dict: The signal data if found, else None.
        """
        keys = path.split(".")
        signal = self.vspec_data
        for key in keys:
            signal = signal.get(key)
            if signal is None:
                logger.warning(f'Signal path "{path}" not found.')
                return None
        return signal
