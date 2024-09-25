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


import os
import sys
import toml
from invoke import run

CONFIG_PATH = "/etc/vss-lib/vss.config"


class PodmanManager:
    def __init__(self, vendor, vspec_file, containerfile):
        self.vendor = vendor
        self.vspec_file = vspec_file
        self.containerfile = containerfile
        self.config = self.load_config(CONFIG_PATH)
        self.vss_lib_path = self.find_vss_lib_path()

    def load_config(self, config_path):
        """
        Load the VSS configuration from a TOML file.
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
            print(f"Configuration file not found: {config_path}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            sys.exit(1)

    def find_vss_lib_path(self):
        """
        Locate the vss-lib Python site-package path.

        Returns:
            str: Path to the vss-lib directory.
        """
        pversion = f"python{sys.version_info.major}.{sys.version_info.minor}"
        site_packages_paths = [
            f"/usr/local/lib/{pversion}/site-packages/vss_lib/",
            f"/usr/lib/{pversion}/site-packages/vss_lib/"
        ]

        print(f"{pversion}")
        print(f"{site_packages_paths}")
        for path in site_packages_paths:
            if os.path.exists(path):
                return path

        print("vss-lib path not found.")
        sys.exit(1)

    def build_container(self):
        """
        Build a Podman container for the specified vendor.
        """
        try:
            command = f"podman build -t {self.vendor}_vss_image -f {self.containerfile} ."
            result = run(command, hide=True, warn=True)
            if result.ok:
                print(f"Container image for {self.vendor} built successfully.")
            else:
                print(f"Failed to build container image for {self.vendor}: {result.stderr}")
                sys.exit(1)
        except Exception as e:
            print(f"Error building Podman container image for {self.vendor}: {e}")
            sys.exit(1)

    def run_container(self):
        """
        Run the Podman container with vendor-specific configurations.
        """
        try:
            vss_spec_path = self.config.get("global", {}).get("vspec_path", "/usr/share/vss-lib")
            run_command = f"""
            podman run -d --replace --name {self.vendor}_vss_container \
              -e STORAGE_DRIVER=vfs \
              --privileged \
              --log-opt max-size=50m \
              --log-opt max-file=3 \
              -v {vss_spec_path}:{vss_spec_path}:Z \
              -v {self.vss_lib_path}:{self.vss_lib_path}:Z \
              -v {self.vspec_file}:/etc/vss-lib/{self.vendor}.vspec:Z \
              -v /etc/vss-lib/vss.config:/etc/vss-lib/vss.config:Z \
              -v /run/dbus/system_bus_socket:/run/dbus/system_bus_socket:Z \
              {self.vendor}_vss_image \
              sh -c "/usr/lib/vss-lib/dbus/container_dbus_service && sleep infinity"
            """
            result = run(run_command, hide=True, warn=True)
            if result.ok:
                print(f"Podman container for {self.vendor} started successfully.")
            else:
                print(f"Failed to start Podman container for {self.vendor}: {result.stderr}")
                sys.exit(1)
        except Exception as e:
            print(f"Error running Podman container for {self.vendor}: {e}")
            sys.exit(1)

    def stop_container(self, container_name=None):
        """
        Stop and remove the Podman container.
        Args:
            container_name (str): The name of the container to stop. If not provided,
                                  it stops the vendor-specific container.
        """
        if not container_name:
            container_name = f"{self.vendor}_vss_container"  # Default to vendor container

        try:
            print(f"Stopping Podman container: {container_name}")
            command = f"podman stop {container_name} && podman rm {container_name}"
            result = run(command, hide=True, warn=True)
            if result.ok:
                print(f"Podman container {container_name} stopped and removed successfully.")
            else:
                print(f"Failed to stop Podman container {container_name}: {result.stderr}")
        except Exception as e:
            print(f"Error stopping Podman container {container_name}: {e}")

    def run_joystick_container(self):
        """
        Run the joystick Podman container using the joystick-specific ContainerFile.
        """
        try:
            vss_spec_path = self.config.get("global", {}).get("vspec_path", "/usr/share/vss-lib")
            run_command = f"""
            podman run -d --replace --name joystick_vss_container \
              -e STORAGE_DRIVER=vfs \
              --privileged \
              --log-opt max-size=50m \
              --log-opt max-file=3 \
              -v {vss_spec_path}:{vss_spec_path}:Z \
              -v {self.vss_lib_path}:{self.vss_lib_path}:Z \
              -v {self.vspec_file}:/etc/vss-lib/{self.vendor}.vspec:Z \
              -v /etc/vss-lib/vss.config:/etc/vss-lib/vss.config:Z \
              -v /run/dbus/system_bus_socket:/run/dbus/system_bus_socket:Z \
              joystick_vss_image \
              sh -c "/usr/lib/vss-lib/dbus/joystick_dbus_service && sleep infinity"
            """
            result = run(run_command, hide=True, warn=True)
            if result.ok:
                print("Podman joystick container started successfully.")
            else:
                print(f"Failed to start Podman joystick container: {result.stderr}")
                sys.exit(1)
        except Exception as e:
            print(f"Error running Podman joystick container: {e}")

    def get_python_site_packages_version(self):
        """
        Retrieve the Python version and return the path for site-packages dynamically.

        Returns:
            str: The full path to /usr/lib/pythonX.Y/site-packages/vss_lib/ where X.Y is the Python version.
        """
        python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        vss_lib_path = f"/usr/lib/{python_version}/site-packages/vss_lib"
        return vss_lib_path
