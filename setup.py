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
import shutil
import subprocess
import sysconfig
from setuptools import setup, find_packages
from setuptools.command.install import install

# Define macros for paths to simplify maintenance
SYSTEMD_DIR = '/lib/systemd/system/'
ETC_DIR = '/etc/vss-lib/'
SHARE_DIR = '/usr/share/vss-lib/'
DBUS_DIR = '/usr/lib/vss-lib/dbus/'
LOG_DIR = '/var/log/vss-lib/'
DBUS_CONF_DIR = '/etc/dbus-1/system.d/'
ELECTRONICS_DIR = os.path.join(SHARE_DIR, 'electronics/')
LATEST_PYTHON_SITE_PACKAGES = sysconfig.get_paths()['purelib']

# Array of individual Python files to copy to LATEST_PYTHON_SITE_PACKAGES
python_files = [
    '__init__.py',
    'base_model.py',
    'config_loader.py',
    'vspec_parser.py',
    'vss_logging.py',
    'vendor_interface.py'
]

# Directories to copy recursively to LATEST_PYTHON_SITE_PACKAGES
directories_to_copy = [
    'client',
    'dbus',
    'vendor',
    'vspec'
]

# Function to remove the existing file and create a new one with the correct content
def create_new_config_file(config_src, config_dst, vspec_path):
    # Remove the existing config file if it exists
    if os.path.exists(config_dst):
        os.remove(config_dst)
        print(f"Removed existing file: {config_dst}")

    # Read the source config file
    with open(config_src, 'r') as file:
        content = file.read()

    # Replace ${vspec_path} with the actual path
    updated_content = content.replace('${vspec_path}', vspec_path)

    # Write the updated content to the new destination file
    with open(config_dst, 'w') as file:
        file.write(updated_content)

    print(f"Created new config file: {config_dst} with vspec_path = {vspec_path}")

# Custom install command to handle file installation and ensure directories exist
class CustomInstallCommand(install):
    def run(self):
        # Run the standard installation process
        install.run(self)

        # Ensure systemd, etc, share, dbus, and log directories exist
        os.makedirs(SYSTEMD_DIR, exist_ok=True)
        os.makedirs(ETC_DIR, exist_ok=True)
        os.makedirs(SHARE_DIR, exist_ok=True)
        os.makedirs(DBUS_DIR, exist_ok=True)
        os.makedirs(LOG_DIR, exist_ok=True)
        os.makedirs(ELECTRONICS_DIR, exist_ok=True)

        print(f"Ensured necessary directories exist")

        # Define the VSS path
        vspec_path = '/usr/share/vss-lib/'

        # Remove and create a new config file
        config_file_src = 'etc/vss-lib/vss.config'
        config_file_dst = os.path.join(ETC_DIR, 'vss.config')
        create_new_config_file(config_file_src, config_file_dst, vspec_path)

        # Copy the logging configuration file to /etc/vss-lib
        shutil.copy('etc/vss-lib/logging.conf', os.path.join(ETC_DIR, 'logging.conf'))
        print(f"Copied logging configuration to {ETC_DIR}")

        # Copy the .vspec files for vehicles to /usr/share/vss-lib
        vspec_files = ['bmw.vspec', 'ford.vspec', 'honda.vspec', 'jaguar.vspec', 'mercedes.vspec', 'toyota.vspec', 'volvo.vspec']
        for vspec in vspec_files:
            shutil.copy(f'usr/share/vss-lib/{vspec}', SHARE_DIR)
            print(f"Copied {vspec} to {SHARE_DIR}")

        # Copy the dbus service file to /usr/lib/vss-lib/dbus
        shutil.copy('src/dbus/container_dbus_service', os.path.join(DBUS_DIR, 'container_dbus_service'))
        print(f"Copied dbus service file to {DBUS_DIR}")

        # Copy the D-Bus configuration file to /etc/dbus-1/system.d
        shutil.copy('etc/dbus-1/system.d/vss-dbus.conf', os.path.join(DBUS_CONF_DIR, 'vss-dbus.conf'))
        print(f"Copied D-Bus configuration to {DBUS_CONF_DIR}")

        # Copy electronics .vspec files from usr/share/vss-lib/electronics/ to /usr/share/vss-lib/electronics/
        electronics_source_dir = 'usr/share/vss-lib/electronics/'
        if os.path.exists(electronics_source_dir):
            for file_name in os.listdir(electronics_source_dir):
                if file_name.endswith('.vspec'):
                    src_file = os.path.join(electronics_source_dir, file_name)
                    dst_file = os.path.join(ELECTRONICS_DIR, file_name)
                    shutil.copy(src_file, dst_file)
                    print(f"Copied {file_name} to {dst_file}")
                else:
                    print(f"{file_name} is not a .vspec file, skipping...")
        else:
            print(f"Directory {electronics_source_dir} does not exist, skipping electronics files...")

        # Define the target directory for Python files using sysconfig's purelib path
        target_dir = os.path.join(LATEST_PYTHON_SITE_PACKAGES, "vss_lib")

        # Ensure target directory exists for Python files
        os.makedirs(target_dir, exist_ok=True)
        print(f"Created {target_dir}")

        # Copy individual Python files to LATEST_PYTHON_SITE_PACKAGES
        for py_file in python_files:
            shutil.copy(f'src/{py_file}', target_dir)
            print(f"Copied {py_file} to {target_dir}")

        # Recursively copy directories and their subdirectories to LATEST_PYTHON_SITE_PACKAGES
        for directory in directories_to_copy:
            src_dir = f'src/{directory}'
            dst_dir = os.path.join(target_dir, directory)
            if os.path.exists(src_dir):
                shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                print(f"Copied {src_dir} to {dst_dir}")
            else:
                print(f"Directory {src_dir} does not exist, skipping...")

        # Reload D-Bus service and enable/start vss-dbus.service
        try:
            subprocess.check_call(['sudo', 'systemctl', 'reload', 'dbus'])
            print("Reloaded D-Bus configuration.")

            subprocess.check_call(['sudo', 'systemctl', 'enable', '--now', 'vss-dbus.service'])
            print("Enabled and started vss-dbus.service.")

        except subprocess.CalledProcessError as e:
            print(f"Failed to reload D-Bus or start service: {e}")
            raise

def check_if_fedora():
    """
    Check if the system is running Fedora by inspecting /etc/os-release or using the rpm command.
    """
    try:
        # Check the operating system by reading /etc/os-release
        result = run("grep -i 'ubuntu' /etc/os-release", warn=True, hide=True)
        if result.ok:
            return True
        return False
    except Exception as e:
        print(f"An error occurred while checking the operating system: {e}")
        return False

# vss-lib was developed under Fedora 40 distro, might need to be adjusted
# to others distros
def check_fuse_overlayfs():
    """
    Check if fuse-overlayfs is installed and recommend installation if it's missing, but only if the system is Fedora.
    """
    if not check_if_fedora():
        print("System is not running Fedora. Skipping fuse-overlayfs check.")
        return

    try:
        # Try to find the fuse-overlayfs package using the rpm command
        result = run("rpm -q fuse-overlayfs", warn=True, hide=True)

        if result.ok:
            print("fuse-overlayfs is installed.")
        else:
            # If the package is not found, recommend installation
            print("fuse-overlayfs is not installed. Please install it using:")
            print("sudo dnf install fuse-overlayfs")
    except Exception as e:
        print(f"An error occurred while checking fuse-overlayfs installation: {e}")

# check fuse_overlayfs package
check_fuse_overlayfs()

# Define the setup for the package
setup(
    name="vss-lib",
    version="0.1.0",
    description="A library for interacting with vehicle signals",
    author="Douglas Schilling Landgraf, Leonardo Rosetti, Yariv Rachmani",
    author_email="dougsland@redhat.com,lrossett@redhat.com,yrachman@redhat.com",
    packages=find_packages(where='src'),  # Find Python packages in src/
    package_dir={'': 'src'},  # Define the package directory for Python files
    python_requires='>=3.10',
    install_requires=[
        "pydbus",
        "toml",
        "pyyaml",
    ],
    cmdclass={
        'install': CustomInstallCommand,  # Custom install command for Python files and system-wide files
    },
)
