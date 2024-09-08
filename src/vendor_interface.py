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

from vss_lib.vspec.model import Model
from vss_lib.vss_logging import logger
from invoke import run

class VehicleSignalInterface:
    """
    Interface to interact with vehicle signal models for different vendors.

    Attributes:
        vendor (str): The vendor for which the interface is created.
        vspec_file (Optional[str]): Path to the VSS file for the vendor, default signals used if not provided.
        preference (Optional[dict]): User preferences for signal generation (e.g., ASIL, QM).
        attached_electronics (list): List of attached electronics vendors.
    """
    def __init__(self, vendor, vspec_file=None, preference=None, attached_electronics=None):
        """
        Initialize the VehicleSignalInterface and start the Podman container for the vendor.
        """
        logger.info(f"Initializing VehicleSignalInterface for vendor={vendor}, vspec_file={vspec_file}")

        self.vendor = vendor.lower()
        self.vspec_file = vspec_file or f"/usr/share/vss-lib/{vendor}.vspec"
        self.preference = preference
        self.attached_electronics = attached_electronics or []

        # Load the VSS model and assign it to self.model
        self.model = self.load_vspec_model(self.vspec_file)

        if not self.model:
            logger.error(f"Failed to load VSS model for {vendor}")
            raise ValueError(f"Model not found for {vendor}")

        # Start the Podman container to run the vss_dbus_service.py
        run_in_podman(self.vendor, self.vspec_file)

        # Attach the electronics after the container is started
        self._attach_electronics()

    def load_vspec_model(self, vspec_file):
        """
        Load the VSS model from the file.

        Args:
            vspec_file (str): The path to the VSS file.

        Returns:
            Model: The loaded VSS model object or None if loading fails.
        """
        try:
            model = Model.from_file(vspec_file)
            logger.info(f"Loaded VSS model from {vspec_file}")
            return model
        except Exception as e:
            logger.error(f"Failed to load VSS model from {vspec_file}: {e}")
            return None

    def _attach_electronics(self):
        """
        Attach electronics vendors to the running container.
        """
        if not self.attached_electronics:
            logger.info("No electronics to attach.")
            return

        logger.info(f"Attaching electronics to {self.vendor} container.")
        # Logic for attaching electronics can go here

    def __del__(self):
        """
        Stop the Podman container when the interface is destroyed.
        """
        stop_podman_container(self.vendor)

    def get_signal_details(self, signal_name):
        """
        Get details of a signal by name.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: A dictionary containing signal details such as datatype, unit, min, and max.
        """
        if not self.model:
            logger.error("VSS model not loaded.")
            return None

        # Traverse the VSS data to get the signal details
        return self.model.get_signal_details(signal_name)

    def validate_signal(self, signal_name, value):
        """
        Validate the value of a signal based on its range.

        Args:
            signal_name (str): The name of the signal.
            value: The value to validate.

        Returns:
            bool: True if the value is within the signal's valid range, else False.
        """
        signal_details = self.get_signal_details(signal_name)
        if signal_details and 'min' in signal_details and 'max' in signal_details:
            if signal_details['min'] <= value <= signal_details['max']:
                logger.info(f"Value {value} for signal '{signal_name}' is valid.")
                return True
            else:
                logger.warning(f"Value {value} for signal '{signal_name}' is out of range.")
                return False
        logger.error(f"Signal '{signal_name}' not found or invalid for validation.")
        return False

# New functions for running and stopping the Podman containers

def run_in_podman(vendor, vspec_file):
    """
    Run the vss_dbus_service.py inside a Podman container for the given vendor.

    Args:
        vendor (str): The vendor for which the container is being created.
        vspec_file (str): The path to the VSS file for the vendor.
    """
    try:
        logger.info(f"Starting Podman container for {vendor}")
        command = f"""
podman run --replace --name toyota_vss_container \
  -v /usr/lib/vss-lib/dbus/vss_dbus_service.py:/usr/lib/vss-lib/dbus/vss_dbus_service.py:Z \
  -v /usr/lib/vss-lib:/usr/lib/vss-lib/:Z \
  -v /etc/vss-lib/vss.config:/etc/vss-lib/vss.config:Z \
  quay.io/podman/stable \
  sh -c "dnf install -y python3-gobject python3-pip && pip3 install pydbus toml pyyaml && python3 /usr/lib/vss-lib/dbus/vss_dbus_service.py"
"""
        logger.warning(command)
        result = run(command, hide=True, warn=True)
        if result.ok:
            logger.info(f"Podman container for {vendor} started successfully.")
        else:
            logger.error(f"Failed to start Podman container for {vendor}: {result.stderr}")
    except Exception as e:
        logger.error(f"Error running Podman container for {vendor}: {e}")

def stop_podman_container(vendor):
    """
    Stop the Podman container for the given vendor.

    Args:
        vendor (str): The vendor for which the container is being stopped.
    """
    try:
        logger.info(f"Stopping Podman container for {vendor}")
        command = f"podman stop {vendor}_vss_container && podman rm {vendor}_vss_container"
        result = run(command, hide=True, warn=True)
        if result.ok:
            logger.info(f"Podman container for {vendor} stopped and removed successfully.")
        else:
            logger.error(f"Failed to stop Podman container for {vendor}: {result.stderr}")
    except Exception as e:
        logger.error(f"Error stopping Podman container for {vendor}: {e}")
