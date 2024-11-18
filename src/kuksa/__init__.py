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

import asyncio
import jwt
import datetime


class KUKSAClientVSS:
    def __init__(self, address='127.0.0.1', port=55555, token=None, secret_key=None):
        self.address = address
        self.port = port
        self.token = token
        self.secret_key = secret_key
        self.client = None
        self.is_authenticated = False
        self.stop_subscription = False

    async def connect(self):
        """Connect to the KUKSA data broker and authenticate if a token is provided."""
        from kuksa_client.grpc.aio import VSSClient  # Lazy import to avoid circular dependency
        self.client = VSSClient(self.address, self.port)
        await self.client.__aenter__()
        print(f"Connected to KUKSA data broker at {self.address}:{self.port}")

        if self.token:
            try:
                jwt.decode(self.token, self.secret_key, algorithms=["HS256"], audience="kuksa.val")
                print("Token is valid.")
                self.is_authenticated = True
            except jwt.InvalidTokenError as e:
                print(f"Error: Invalid token. Details: {e}")
                print("Client did not send a valid token to authenticate. Access denied.")
                return
            await self.client.authorize(self.token)
            print("Authentication successful.")
        else:
            print("No token provided. Proceeding without authentication.")

    async def disconnect(self):
        """Disconnect from the KUKSA data broker."""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None
            print("Disconnected from KUKSA data broker.")

    async def set_signal_value(self, signal_path, value):
        """Set a value for a specified signal."""
        if self.token and not self.is_authenticated:
            print("Client is not authenticated. Cannot set signal value.")
            return

        if not self.client:
            raise ConnectionError("Client is not connected. Call connect() first.")

        from kuksa_client.grpc import Datapoint, DataEntry, EntryUpdate, Metadata, Field, DataType  # Lazy import

        updates = (EntryUpdate(DataEntry(
            signal_path,
            value=Datapoint(value=value),
            metadata=Metadata(data_type=DataType.FLOAT)
        ), (Field.VALUE,)),)

        await self.client.set(updates=updates)
        print(f"Set value {value} for signal '{signal_path}'")

    async def subscribe_to_signal(self, signal_path, timeout=5):
        """
        Subscribe to updates for a specified signal and print changes with a timeout.
        :param signal_path: The VSS signal path to subscribe to.
        :param timeout: Duration (in seconds) to allow the subscription to run.
        """
        if self.token and not self.is_authenticated:
            print("Client is not authenticated. Cannot subscribe to signal updates.")
            return

        print(f"Subscribing to updates for '{signal_path}'...")

        async def subscription_task():
            async for updates in self.client.subscribe_current_values([signal_path]):
                if self.stop_subscription:
                    print(f"Stopping subscription to '{signal_path}'.")
                    break
                if updates.get(signal_path) is not None:
                    value = updates[signal_path].value
                    print(f"Received update for '{signal_path}': {value}")
                else:
                    print(f"No update for '{signal_path}' or received 'None'")

        # Run the subscription task with a timeout
        task = asyncio.create_task(subscription_task())
        try:
            await asyncio.wait_for(task, timeout=timeout)
        except asyncio.TimeoutError:
            print(f"Subscription to '{signal_path}' timed out after {timeout} seconds.")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print(f"Subscription task for '{signal_path}' was cancelled.")


async def authorized_client():
    print("\n=== Authorized Client ===")
    secret_key = "your-256-bit-secret"
    payload = {
        "sub": "test-client",
        "iss": "your-issuer",
        "aud": "kuksa.val",
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    client = KUKSAClientVSS(token=token, secret_key=secret_key)
    await client.connect()

    if client.is_authenticated:
        signal_path = 'Vehicle.Speed'
        await client.set_signal_value(signal_path, 50)
        await client.subscribe_to_signal(signal_path, timeout=5)  # Subscribe with a 5-second timeout

    await client.disconnect()
