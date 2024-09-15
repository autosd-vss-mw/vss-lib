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
