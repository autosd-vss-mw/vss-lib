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
import sys
import toml
from vss_lib.vspec.model import Model
from vss_lib.vss_logging import logger
from invoke import run
from vss_lib.canbus import CANBusSimulator

CONFIG_PATH = '/etc/vss-lib/vss.config'

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

        # Initialize CANBusSimulator
        self.canbus_simulator = CANBusSimulator()

        # Load the VSS model and assign it to self.model
        self.model = self.load_vspec_model(self.vspec_file)

        if not self.model:
            logger.error(f"Failed to load VSS model for {vendor}")
            raise ValueError(f"Model not found for {vendor}")

        # Start the Podman container to run the container_dbus_service
        run_in_podman(self.vendor, self.vspec_file)

        # Attach the electronics after the container is started
        self._attach_electronics()

    def load_vspec_model(self, vspec_file):
        """
        Load the VSS model from the file and print the contents for debugging if errors occur.

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
            # Print the full path and contents of the VSS file for debugging
            if os.path.exists(vspec_file):
                logger.error(f"Full path of the VSS file: {os.path.abspath(vspec_file)}")
                with open(vspec_file, 'r') as file:
                    vss_content = file.read()
                    logger.error(f"VSS file content for {vspec_file}:\n{vss_content}")
            else:
                logger.error(f"VSS file {vspec_file} does not exist.")
            return None

    def _attach_electronics(self):
        """
        Attach electronics vendors to the running container.
        """
        if not self.attached_electronics:
            logger.info("No electronics to attach.")
            return
        logger.info(f"Attaching electronics to {self.vendor} container.")
        for electronics in self.attached_electronics:
            logger.info(f"Simulating CAN message for attached electronics: {electronics}")
            # Simulate encoding and decoding CAN messages for each attached electronic vendor
            self.simulate_can_message("attach_electronics", electronics)

    def get_signal_details(self, signal_name):
        """
        Retrieve the details of a specific signal.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: The details of the signal, or None if the signal is not found.
        """
        if not self.model:
            logger.error("VSS model not loaded.")
            return None
        return self.model.get_signal_details(signal_name)

    def validate_signal(self, signal_name, value):
        """
        Validate the value of a signal based on its range and datatype.

        Args:
            signal_name (str): The name of the signal.
            value: The value to validate.

        Returns:
            bool: True if the value is within the signal's valid range, else False.
        """
        signal_details = self.get_signal_details(signal_name)
        if signal_details:
            unit = signal_details.get('unit', None)
            min_value = signal_details.get('min', 0)
            max_value = signal_details.get('max', 100)

            if min_value <= value <= max_value:
                logger.info(f"Value {value} for signal '{signal_name}' is valid (min: {min_value}, max: {max_value}, unit: {unit if unit is not None else 'none'}).")
                # Simulate CAN message encoding and decoding on valid signals
                self.simulate_can_message(signal_name, value)
                return True
            else:
                logger.warning(f"Value {value} for signal '{signal_name}' is out of range (min: {min_value}, max: {max_value}, unit: {unit if unit is not None else 'none'}).")
                return False
        logger.error(f"Signal '{signal_name}' not found or invalid for validation.")
        return False

    def simulate_can_message(self, signal_name, value):
        """
        Simulate encoding and decoding a CAN message for the given signal and value.

        Args:
            signal_name (str): The name of the signal.
            value: The value to encode in the CAN message.
        """
        data = {"signal": signal_name, "value": value}
        encoded_message = self.canbus_simulator.encode_can_message(data)
        self.canbus_simulator.decode_can_message(encoded_message)


def load_config(config_path):
    """
    Load the TOML configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration data.
    """
    try:
        with open(config_path, 'r') as config_file:
            config = toml.load(config_file)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        return None


def get_python_version():
    """
    Get the current Python version in the format pythonX.Y.

    Returns:
        str: The current Python version (e.g., python3.8).
    """
    return f"python{sys.version_info.major}.{sys.version_info.minor}"


def find_vss_lib_path(config):
    """
    Find the first valid vss-lib path based on the configuration.

    Args:
        config (dict): The parsed TOML configuration.

    Returns:
        str: The first valid path to the vss-lib directory, or None if not found.
    """
    python_version = get_python_version()
    vss_lib_search_paths = config.get("global", {}).get("vss_lib_search_paths", [])

    for path in vss_lib_search_paths:
        path = path.replace("{python_version}", python_version)
        if os.path.exists(path):
            logger.info(f"Found vss-lib in: {path}")
            return path
    logger.error("vss-lib not found in any of the search paths.")
    return None


def get_python_version_path():
    """
    Retrieve the Python version and return the path for site-packages dynamically.

    Returns:
        str: The full path to /usr/lib/pythonX.Y/site-packages/vss_lib/ where X.Y is the Python version.
    """
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    vss_lib_path = f"/usr/lib/{python_version}/site-packages/vss_lib"
    return vss_lib_path

def run_in_podman(vendor, vspec_file):
    """
    Run the container_dbus_service inside a Podman container for the given vendor.

    Args:
        vendor (str): The vendor for which the container is being created.
        vspec_file (str): The path to the VSS file for the vendor.
    """
    # Load configuration
    config = load_config(CONFIG_PATH)
    if not config:
        logger.error(f"Failed to load the configuration for {vendor}.")
        sys.exit(1)

    # Locate the current installation of vss-lib python site-package
    vss_lib_path = find_vss_lib_path(config)
    if not vss_lib_path:
        logger.error(f"vss-lib path not found for {vendor}.")
        sys.exit(1)

    vss_spec_path = config.get("global", {}).get("vspec_path", "/usr/share/vss-lib")
    containerfile_dbus_manager = config.get("global", {}).get("containerfile_dbus_manager", "/usr/share/vss-lib/Containerfile")

    # Get current Python version path
    python_site_packages_vss_lib = get_python_version_path()

    # Step 1: Build the container image
    try:
        logger.info(f"Building Podman container image...")
        build_command = f"podman build -t {vendor}_vss_image -f {containerfile_dbus_manager} ."
        build_result = run(build_command, hide=True, warn=True)
        if build_result.ok:
            logger.info(f"Container image for {vendor} built successfully.")
        else:
            logger.error(f"Failed to build container image for {vendor}: {build_result.stderr}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error building Podman container image for {vendor}: {e}")
        sys.exit(1)

    # Step 2: Run the container with vendor-specific configurations
    try:
        logger.info(f"Starting Podman container for {vendor}")
        run_command = f"""
        podman run -d --replace --name {vendor}_vss_container \
          -e STORAGE_DRIVER=vfs \
          --privileged \
          --log-opt max-size=50m \
          --log-opt max-file=3 \
          -v {vss_spec_path}:{vss_spec_path}:Z \
          -v {vss_lib_path}:{python_site_packages_vss_lib}:Z \
          -v {vspec_file}:/etc/vss-lib/{vendor}.vspec:Z \
          -v /etc/vss-lib/vss.config:/etc/vss-lib/vss.config:Z \
          -v /run/dbus/system_bus_socket:/run/dbus/system_bus_socket:Z \
          {vendor}_vss_image \
          sh -c "/usr/lib/vss-lib/dbus/container_dbus_service && sleep infinity"
        """
        logger.info(f"Running command for {vendor}: {run_command}")
        run_result = run(run_command, hide=True, warn=True)
        if run_result.ok:
            logger.info(f"Podman container for {vendor} started successfully.")
        else:
            logger.error(f"Failed to start Podman container for {vendor}: {run_result.stderr}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error running Podman container for {vendor}: {e}")
        sys.exit(1)

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
