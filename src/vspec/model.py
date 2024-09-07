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

from vss_lib.vss_logging import logger
import yaml

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
        self.signals = self._extract_signals()  # Extract signals upon initialization

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
                data = yaml.safe_load(file)
                logger.info(f'Successfully loaded VSS file: {vspec_file}')
                return cls(data)
        except FileNotFoundError:
            logger.error(f'VSS file not found: {vspec_file}')
            return None
        except yaml.YAMLError as e:
            logger.error(f'Error decoding YAML in VSS file {vspec_file}: {e}')
            return None
        except PermissionError:
            logger.error(f'Permission denied when accessing VSS file: {vspec_file}')
            return None

    def _extract_signals(self):
        """
        Extract signals from the loaded VSS data.

        Returns:
            dict: A dictionary of signals extracted from the VSS data.
        """
        signals = {}
        if 'Vehicle' in self.vspec_data:
            for signal_name, details in self.vspec_data['Vehicle'].items():
                signals[signal_name] = details
        return signals

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
