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


    def get_signal_details(self, signal_name):
        """
        Get details of a signal by name from the VSS data.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: A dictionary containing signal details such as datatype, unit, min, and max,
                  or None if the signal is not found or the format is unexpected.
        """
        if not self.vspec_data:
            return None

        # Split the signal path and traverse the VSS data structure
        signal_parts = signal_name.split('.')
        current_data = self.vspec_data

        for part in signal_parts:
            if part in current_data:
                current_data = current_data[part]
            else:
                logger.warning(f"Signal '{signal_name}' not found in VSS data.")
                return None

        # If the signal is found but is a string or number, wrap it in a dictionary for consistency
        if isinstance(current_data, (str, int, float)):
            logger.warning(f"Signal details for '{signal_name}' are not in expected dictionary format.")
            return {"value": current_data}

        # Ensure the data is a dictionary before returning
        if isinstance(current_data, dict):
            return current_data

        # Log an error if the signal is not in the expected format
        logger.error(f"Signal details for '{signal_name}' are not in the expected format.")
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
    
        # Ensure we start looking under the 'Vehicle' key if present
        signal = self.vspec_data.get('Vehicle', {})
        partial_path = "Vehicle"

        for i, key in enumerate(keys):
            if isinstance(signal, dict) and key in signal:
                signal = signal[key]
                partial_path += f".{key}"
                logger.info(f"Found part of the path: {partial_path}")
            else:
                logger.warning(f'Key "{key}" not found in "{partial_path}".')
                if isinstance(signal, dict):
                    available_keys = list(signal.keys())
                    logger.info(f"Available keys at this level: {available_keys}")
                return None

        logger.info(f"Complete signal path found: {path}")
        return signal

