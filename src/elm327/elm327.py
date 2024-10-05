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

import serial
import time


class ELM327:
    """
    A class to interact with an ELM327 OBD-II adapter over a serial connection.

    This is not a CAN bus sniffer. The ELM327 abstracts raw CAN data
    and provides access only to specific OBD-II parameters. It is designed for
    querying diagnostic information from the vehicle's ECU.

    Attributes:
        port (str): The serial port where the ELM327 device is connected (e.g., `/dev/ttyUSB0`).
        baudrate (int): The baud rate for the serial communication (usually 38400 for ELM327).
        timeout (int or float): The timeout for reading responses from the ELM327.
        ser (serial.Serial): The serial connection to the ELM327 device.
    """

    # Protocol commands
    PROTOCOL_CAN = b'ATSP6\r'  # ISO 15765-4 CAN (11-bit ID, 500 kbps)
    PROTOCOL_ISO_9141 = b'ATSP3\r'  # ISO 9141-2
    PROTOCOL_KWP2000 = b'ATSP4\r'  # ISO 14230-4 KWP (5 baud init)
    PROTOCOL_KWP2000_FAST = b'ATSP5\r'  # ISO 14230-4 KWP (fast init)
    PROTOCOL_J1850_PWM = b'ATSP1\r'  # SAE J1850 PWM (Ford)
    PROTOCOL_J1850_VPW = b'ATSP2\r'  # SAE J1850 VPW (GM)
    PROTOCOL_CAN_29BIT = b'ATSP7\r'  # ISO 15765-4 CAN (29-bit ID, 250 kbps)
    PROTOCOL_AUTO = b'ATSP0\r'  # Automatic protocol detection

    # General commands
    RESET_COMMAND = b'ATZ\r'  # Reset the ELM327 device
    SHOW_HEADERS_COMMAND = b'ATH1\r'  # Show CAN message headers
    SUPPORTED_PIDS_COMMAND = b'0100\r'  # Request supported PIDs
    RPM_COMMAND = b'010C\r'  # Request engine RPM
    SPEED_COMMAND = b'010D\r'  # Request vehicle speed
    FUEL_LEVEL_COMMAND = b'012F\r'  # Request fuel level
    CLEAR_DTC_COMMAND = b'04\r'  # Clear diagnostic trouble codes (DTCs)
    CHECK_DTC_COMMAND = b'03\r'  # Check for diagnostic trouble codes (DTCs)
    VIN_COMMAND = b'0902\r'  # Request VIN
    BATTERY_VOLTAGE_COMMAND = b'ATRV\r'  # Request battery voltage
    THROTTLE_POSITION_COMMAND = b'0111\r'  # Request throttle position
    COOLANT_TEMP_COMMAND = b'0105\r'  # Request coolant temperature
    AIR_INTAKE_TEMP_COMMAND = b'010F\r'  # Request air intake temperature
    FUEL_PRESSURE_COMMAND = b'010A\r'  # Request fuel pressure
    FUEL_SYSTEM_STATUS_COMMAND = b'0103\r'  # Request fuel system status
    FUEL_CONSUMPTION_COMMAND = b'015E\r'  # Request fuel consumption
    ENGINE_LOAD_COMMAND = b'0104\r'  # Request engine load

    def __init__(self, port='/dev/ttyUSB0', baudrate=38400, timeout=1):
        """
        Initialize the ELM327 object and open the serial connection.

        Args:
            port (str): The serial port where the ELM327 device is connected (default `/dev/ttyUSB0`).
            baudrate (int): The baud rate for the serial connection (default 38400).
            timeout (int or float): The timeout duration for reading responses (default 1 second).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def reset(self):
        """
        Reset the ELM327 device by sending the ATZ command.

        Returns:
            str: The response from the ELM327 device after the reset command.
        """
        self.ser.write(self.RESET_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def show_headers(self):
        """
        Enable displaying CAN message headers by sending the ATH1 command.

        Returns:
            str: The response from the ELM327 device after enabling headers.
        """
        self.ser.write(self.SHOW_HEADERS_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_can(self):
        self.ser.write(self.PROTOCOL_CAN)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_iso_9141(self):
        self.ser.write(self.PROTOCOL_ISO_9141)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_kwp2000(self):
        self.ser.write(self.PROTOCOL_KWP2000)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_kwp2000_fast(self):
        self.ser.write(self.PROTOCOL_KWP2000_FAST)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_j1850_pwm(self):
        self.ser.write(self.PROTOCOL_J1850_PWM)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_j1850_vpw(self):
        self.ser.write(self.PROTOCOL_J1850_VPW)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_can_29bit(self):
        self.ser.write(self.PROTOCOL_CAN_29BIT)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def set_protocol_auto(self):
        self.ser.write(self.PROTOCOL_AUTO)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_supported_pids(self):
        self.ser.write(self.SUPPORTED_PIDS_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_rpm(self):
        self.ser.write(self.RPM_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_speed(self):
        self.ser.write(self.SPEED_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_fuel_level(self):
        self.ser.write(self.FUEL_LEVEL_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def clear_dtc(self):
        self.ser.write(self.CLEAR_DTC_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def check_dtc(self):
        self.ser.write(self.CHECK_DTC_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_vin(self):
        """
        Request the Vehicle Identification Number (VIN) by sending the 0902 command.

        Returns:
            str: The VIN as reported by the vehicle's ECU.
        """
        self.ser.write(self.VIN_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_battery_voltage(self):
        """
        Request the battery voltage by sending the ATRV command.

        Returns:
            str: The battery voltage as reported by the ELM327 device.
        """
        self.ser.write(self.BATTERY_VOLTAGE_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_throttle_position(self):
        """
        Request the throttle position by sending the 0111 command.

        Returns:
            str: The throttle position as a percentage.
        """
        self.ser.write(self.THROTTLE_POSITION_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_coolant_temperature(self):
        """
        Request the engine coolant temperature by sending the 0105 command.

        Returns:
            str: The engine coolant temperature in degrees Celsius.
        """
        self.ser.write(self.COOLANT_TEMP_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_air_intake_temperature(self):
        """
        Request the air intake temperature by sending the 010F command.

        Returns:
            str: The air intake temperature in degrees Celsius.
        """
        self.ser.write(self.AIR_INTAKE_TEMP_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_fuel_pressure(self):
        """
        Request the fuel pressure by sending the 010A command.

        Returns:
            str: The fuel pressure as reported by the ECU.
        """
        self.ser.write(self.FUEL_PRESSURE_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_fuel_system_status(self):
        """
        Request the fuel system status by sending the 0103 command.

        Returns:
            str: The fuel system status as reported by the ECU.
        """
        self.ser.write(self.FUEL_SYSTEM_STATUS_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_fuel_consumption(self):
        """
        Request the real-time fuel consumption rate by sending the 015E command.

        Returns:
            str: The fuel consumption rate as reported by the ECU.
        """
        self.ser.write(self.FUEL_CONSUMPTION_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def get_engine_load(self):
        """
        Request the engine load by sending the 0104 command.

        Returns:
            str: The engine load as reported by the ECU.
        """
        self.ser.write(self.ENGINE_LOAD_COMMAND)
        time.sleep(1)
        return self.ser.read(128).decode('utf-8')

    def close(self):
        """
        Close the serial connection to the ELM327 device.

        Returns:
            None
        """
        self.ser.close()
