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

import can
import time


class CANBusMonitor:
    """
    A class to monitor CAN bus traffic and filter messages by vendor or message type.

    Attributes:
    -----------
    interface : str
        The CAN interface to monitor (e.g., 'vcan0').
    bus : can.Bus
        The CAN bus object used to interface with the CAN network.
    message_log : list
        Stores the most recent CAN messages for display.
    current_vendor : str
        The currently selected vendor to filter CAN messages by.
    current_message_type : str
        The currently selected message type to filter CAN messages by.
    """

    # Predefined vendor CAN IDs
    VENDORS = {
        "toyota": ["2F0", "300", "40D"],
        "bmw": ["1D0", "2F9", "1F2"],
        "ford": ["3E9", "2D0", "29A"],
        "honda": ["188", "1D5", "17C"],
        "nissan": ["1DA", "285", "390"],
        "gm": ["7E0", "7E8", "102"],
        "gmc": ["13F", "142", "1A2"],
        "volvo": ["23A", "1A5", "345"],
        "audi": ["19D", "2DF", "38C"],
        "mercedes": ["345", "240", "290"],
        "tesla": ["108", "388", "48A"]
    }

    # Predefined message types for each vendor
    MESSAGE_TYPES = {
        "toyota": {
            "engine": ["2F0", "300"],
            "radio": ["40D"],
            "transmission": ["4E0"]
        },
        "bmw": {
            "engine": ["1D0"],
            "iDrive": ["2F9"],
            "transmission": ["1F2"]
        },
        "ford": {
            "engine": ["3E9"],
            "radio": ["2D0"],
            "transmission": ["29A"]
        },
        "honda": {
            "engine": ["188"],
            "infotainment": ["1D5"],
            "transmission": ["17C"]
        },
        "nissan": {
            "engine": ["1DA"],
            "battery": ["285"],
            "climate_control": ["390"]
        },
        "gm": {
            "engine": ["7E0"],
            "infotainment": ["7E8"],
            "transmission": ["102"]
        },
        "gmc": {
            "engine": ["13F"],
            "transmission": ["142"],
            "infotainment": ["1A2"]
        },
        "volvo": {
            "engine": ["23A"],
            "transmission": ["1A5"],
            "infotainment": ["345"]
        },
        "audi": {
            "engine": ["19D"],
            "transmission": ["2DF"],
            "infotainment": ["38C"]
        },
        "mercedes": {
            "engine": ["345"],
            "transmission": ["240"],
            "infotainment": ["290"]
        },
        "tesla": {
            "engine": ["108"],
            "battery": ["388"],
            "climate_control": ["48A"]
        }
    }

    def __init__(self, interface: str):
        """
        Initializes the CANBusMonitor class with the specified CAN interface.

        Parameters:
        -----------
        interface : str
            The CAN interface to monitor (e.g., 'vcan0').
        """
        self.interface = interface
        self.bus = can.interface.Bus(channel=self.interface, bustype='socketcan')
        self.message_log = []
        self.current_vendor = None
        self.current_message_type = None

    def read_can_messages(self):
        """
        Reads CAN messages from the bus and filters them based on the current vendor
        and message type.
        """
        while True:
            msg = self.bus.recv(1.0)  # Receive a message with a timeout of 1 second
            if msg is not None:
                can_id = f"{msg.arbitration_id:X}"
                data = msg.data.hex()

                # Check for vendor filtering
                if self.current_vendor and can_id not in self.VENDORS.get(self.current_vendor, []):
                    continue

                # Check for message type filtering
                if self.current_message_type and can_id not in self.MESSAGE_TYPES.get(self.current_vendor, {}).get(self.current_message_type, []):
                    continue

                # Log the message
                timestamp = time.time()
                self.message_log.append(f"{timestamp:.2f} {can_id} {data}")
                if len(self.message_log) > 10:
                    self.message_log.pop(0)

    def set_vendor(self, vendor: str):
        """
        Set the current vendor for filtering.

        Parameters:
        -----------
        vendor : str
            The vendor to filter by (e.g., 'toyota').
        """
        self.current_vendor = vendor

    def set_message_type(self, message_type: str):
        """
        Set the current message type for filtering.

        Parameters:
        -----------
        message_type : str
            The message type to filter by (e.g., 'engine').
        """
        self.current_message_type = message_type
