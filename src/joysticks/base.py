#!/usr/bin/env python3
# flake8: noqa: E501
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

import pygame
from pydbus import SystemBus
from vss_lib.vss_logging import logger

class JoystickController:
    def __init__(self, log_file=None):
        """
        Initializes the Joystick Controller and sets up D-Bus client and logging.
        If log_file is None, logs will not be saved to a file.
        """
        # Initialize pygame
        pygame.init()
        pygame.joystick.init()

        # Initialize the D-Bus client
        self.bus = SystemBus()
        self.vss_service = self.bus.get("com.vss_lib.VehicleSignals")

        # Check if any joystick is connected
        if pygame.joystick.get_count() == 0:
            logger.error("No joystick found")
            sys.exit()

        # Initialize the first joystick
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Log the detected joystick
        logger.info(f"Joystick detected: {self.joystick.get_name()}")

    def send_signal_to_dbus(self, signal_name, value):
        """
        Sends the joystick signal to D-Bus.
        """
        try:
            self.vss_service.EmitHardwareSignal(signal_name, value)
            logger.info(f"Signal '{signal_name}' with value {value} sent.")
        except Exception as e:
            logger.error(f"Failed to send signal '{signal_name}' to D-Bus: {e}")

    def log_and_send_signal(self, signal_name, value):
        """
        Logs the event and sends a corresponding D-Bus signal.
        """
        # Log the event
        logger.info(f"{signal_name} with value: {value}")

        # Send the signal to D-Bus
        self.send_signal_to_dbus(signal_name, value)

    def log_event(self, event):
        """
        Logs joystick events and sends corresponding signals to D-Bus.
        """
        if event.type == pygame.JOYAXISMOTION:
            # Log axis movement and send to D-Bus
            self.log_and_send_signal(f"Axis {event.axis} moved", event.value)
        elif event.type == pygame.JOYBUTTONDOWN:
            # Log button press and send to D-Bus
            self.log_and_send_signal(f"Button {event.button} pressed", 1)
        elif event.type == pygame.JOYBUTTONUP:
            # Log button release and send to D-Bus
            self.log_and_send_signal(f"Button {event.button} released", 0)
        elif event.type == pygame.JOYHATMOTION:
            # Log D-pad (hat) movement and send to D-Bus
            self.log_and_send_signal(f"Hat {event.hat} moved", event.value)

    def listen(self):
    """
    Listens for joystick events and logs them.
    """
    try:
        logger.info("Joystick listening started...")
        while True:
            events = pygame.event.get()
            if events:
                logger.debug(f"Events detected: {events}")
            for event in events:
                self.log_event(event)
    except KeyboardInterrupt:
        logger.info("Joystick listening interrupted and exited.")
    finally:
        pygame.quit()
        logger.info("Joystick and pygame quit successfully.")

# BaseModel updated to initialize the joystick controller
class BaseModel:
    """
    Base class for handling common signal operations across different vendors.
    """

    def __init__(self, vspec_file, vendor, preference, attached_electronics):
        """
        Initialize the model by loading the specified VSS file and setting up the vehicle interface.
        Also initializes the JoystickController.
        """
        # Initialize JoystickController when the program starts
        self.joystick_controller = JoystickController()
        self.joystick_controller.listen()

        # Ensure vspec_file is a full path
        if not os.path.isabs(vspec_file):
            vspec_file = f"/usr/share/vss-lib/{vspec_file}.vspec"

        self.vspec_file = vspec_file
        self.vspec_data = load_vspec_file(vspec_file)

        if self.vspec_data is None:
            raise AttributeError(f"Failed to load model from {vspec_file}")

        logger.info(f'Loaded VSS model from {vspec_file}')

        # Initialize VehicleSignalInterface for the vendor
        try:
            self.vehicle_signal_interface = VehicleSignalInterface(
                vendor=vendor, preference=preference, attached_electronics=attached_electronics
            )
            logger.info(f"VehicleSignalInterface initialized for {vendor}.")
        except Exception as e:
            logger.error(f"Failed to initialize VehicleSignalInterface for {vendor}: {e}")
            self.vehicle_signal_interface = None

        # Load available signals
        self.available_signals = self.load_available_signals()

    def load_available_signals(self):
        """
        Load and return the available signals from the model.

        Returns:
            list: A list of signal paths available in the model.
        """
        if self.vspec_data is None:
            raise AttributeError("BaseModel has no 'vspec_data' initialized.")

        return list(self.vspec_data.keys()) if self.vspec_data else []

    def attach_electronic(self, electronic_model):
        """
        Attach an electronics vendor to the car vendor.

        Args:
            electronic_model (object): The electronics model to attach.
        """
        self.attached_electronics.append(electronic_model)
        logger.info(f'Attached {electronic_model.__class__.__name__} to {self.__class__.__name__}')

    def get_signal_details(self, signal_name):
        """
        Get details of a signal by name.

        Args:
            signal_name (str): The name of the signal to retrieve details for.

        Returns:
            dict: A dictionary containing signal details such as datatype,
                  unit, min, and max.
        """
        keys = signal_name.split(".")
        signal = self.vspec_data  # This is the loaded VSS model

        for key in keys:
            if isinstance(signal, dict):
                signal = signal.get(key)
            else:
                logger.error(f"Expected dictionary for signal path '{signal_name}', but got: {type(signal)}")
                return None

            if signal is None:
                logger.warning(f"Signal path '{signal_name}' not found.")
                return None

        # Ensure the signal is a dictionary and not an int or other type
        if not isinstance(signal, dict):
            logger.error(f"Expected signal details for '{signal_name}', but got: {type(signal)}")
            return None

        return {
            "datatype": signal.get('datatype'),
            "unit": signal.get('unit'),
            "min": signal.get('min'),
            "max": signal.get('max')
        }

    def validate_signal(self, signal_name, value):
        """
        Validate the signal value for any model.

        Args:
            signal_name (str): The name of the signal.
            value: The value to validate.

        Returns:
            bool: True if the value is valid, else False.
        """
        signal = self.get_signal_details(signal_name)
        if signal:
            if signal.get('min') <= value <= signal.get('max'):
                logger.info(f'Value {value} for signal "{signal_name}" is valid.')
                return True
            else:
                logger.warning(f'Value {value} for signal "{signal_name}" is out of range.')
                return False
        logger.error(f'Signal "{signal_name}" not found for validation.')
        return False
