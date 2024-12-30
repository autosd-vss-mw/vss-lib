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

class UProtocol:
    """
    Handles uProtocol encoding and decoding.
    """

    @staticmethod
    def encode_signal(signal_name: str, value: any) -> bytes:
        """
        Encodes a signal into uProtocol format.
        :param signal_name: Name of the signal
        :param value: Value of the signal
        :return: Encoded bytes
        """
        return f"{signal_name}:{value}".encode('utf-8')

    @staticmethod
    def decode_signal(encoded_data: bytes) -> tuple:
        """
        Decodes uProtocol data.
        :param encoded_data: Encoded uProtocol message
        :return: Tuple containing signal name and value
        """
        decoded_str = encoded_data.decode('utf-8')
        signal_name, value = decoded_str.split(':')
        return signal_name, value

    @staticmethod
    def send_message(message: bytes, destination: str) -> None:
        """
        Simulates sending a uProtocol message to a destination.
        :param message: Encoded message
        :param destination: Target address
        """
        print(f"Sending uProtocol message to {destination}: {message}")

    @staticmethod
    def receive_message(source: str) -> bytes:
        """
        Simulates receiving a uProtocol message from a source.
        :param source: Source address
        :return: Received message
        """
        print(f"Receiving uProtocol message from {source}")
        # Example placeholder message
        return b"ExampleSignal:42"
