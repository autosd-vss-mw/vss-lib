# VSS Middleware and Kuksa

`VSS Middleware` designed to encapsulate all necessary modules to address the signal management needs of vehicles comprehensively. By leveraging the power of the Vehicle Signal Specification (VSS), it enables seamless interaction with vehicle signals across various models and electronics. [KUKSA](https://github.com/eclipse-kuksa) offers capabilities for managing vehicle signals and it's integrated too.

## Table of Contents

1. [Key Features and Functionalities](#key-features-and-functionalities)
2. [Why KUKSA?](#why-kuksa)
3. [Installation](#installation)
4. [Setting Up the KUKSA Data Broker with Podman](#setting-up-the-kuksa-data-broker-with-podman)
   - [Prerequisites](#prerequisites)
   - [Running the KUKSA Data Broker with Podman](#running-the-kuksa-data-broker-with-podman)
5. [Connecting to the KUKSA Broker Using VSS Middleware](#connecting-to-the-kuksa-broker)
6. [Additional Notes](#additional-notes)

## Key Features and Functionalities

- **Middleware for Vehicle Signals**: `VSS Middleware` serves as a central layer that bridges different modules and provides unified functionality for managing signals in automotive systems.
- **Signal Retrieval and Subscription**: Effortlessly retrieve and subscribe to vehicle signals using VSS-compliant paths.
- **Vendor and Model Support**: Attach and configure multiple vendors, vehicle models, and electronics with ease.
- **Compatibility and Extensibility**: Built to integrate with various hardware platforms, simulation environments, and real-time systems.
- **Integration with KUKSA Data Broker**: Provides built-in support for the [KUKSA Data Broker](https://github.com/eclipse/kuksa.val), enabling standardized interaction with signals based on the [COVESA Vehicle Signal Specification](https://www.covesa.global/vss).

## Installation

To install `vss middleware`, use the following command:

```bash
git clone https://github.com/autosd-vss-mw/vss-lib.git
cd vss-lib
make
```

## Setting Up the KUKSA Data Broker with Podman

The KUKSA Data Broker acts as a central hub for vehicle signals and can be easily deployed using `Podman`.

### Prerequisites

Ensure that `Podman` is installed. Refer to the [Podman installation guide](https://podman.io/getting-started/installation) if needed.

### Running the KUKSA Data Broker with Podman

1. **Pull the KUKSA Data Broker image**:
   ```bash
   podman pull ghcr.io/eclipse/kuksa.val/databroker:latest
   ```

2. **Run the Data Broker container**:
   ```bash
   podman run -d --name kuksa-broker -p 55555:55555 ghcr.io/eclipse/kuksa.val/databroker:latest
   ```
   - The container runs in detached mode.
   - Port `55555` is exposed for communication with the broker.

3. **Verify that the Data Broker is Running**:
   Use the following command to verify:
   ```bash
   podman ps
   ```
   You should see a running container named `kuksa-broker`.

## Connecting to the KUKSA Broker

After setting up the KUKSA Data Broker, you can connect to it using the `VSS Middleware` client:

```bash
$ cd examples/kuksa
$ ./set_read_values_from_subscribe
Connected to KUKSA data broker at 127.0.0.1:55555
Subscribing to updates for 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition'...
Set value 45 for signal 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition'
Received update for 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition': 45.0
Received update for 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition': 46.0
Set value 46 for signal 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition'
Received update for 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition': 47.0
Set value 47 for signal 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition'
Received update for 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition': 48.0
Set value 48 for signal 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition'
^CSignal updater task was cancelled.
Main task was cancelled.
Disconnected from KUKSA data broker.
```

```python
import asyncio
from vss_lib.kuksa import KUKSAClientVSS

async def signal_updater(client, signal_path, initial_value):
    """Continuously update the signal value."""
    value = initial_value
    try:
        for _ in range(5):  # Update 5 times for demonstration
            await client.set_signal_value(signal_path, value)
            value += 1
            await asyncio.sleep(2)  # Wait before updating again
    except asyncio.CancelledError:
        print("Signal updater task was cancelled.")

async def main():
    client = KUKSAClientVSS()
    await client.connect()

    # Signal path to use for testing
    signal_path = 'Vehicle.Body.Windshield.Front.Wiping.System.TargetPosition'

    # Create concurrent tasks for updating and subscribing
    updater_task = asyncio.create_task(signal_updater(client, signal_path, 45))
    subscriber_task = asyncio.create_task(client.subscribe_to_signal(signal_path))

    try:
        # Run tasks concurrently
        await asyncio.gather(updater_task, subscriber_task)
    except asyncio.CancelledError:
        print("Main task was cancelled.")
    finally:
        await client.disconnect()

# Run the main function with a graceful shutdown on KeyboardInterrupt
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program interrupted by user. Exiting gracefully.")
```

## Additional Notes

- Replace `127.0.0.1` and `55555` with the appropriate address and port for your KUKSA Data Broker instance if it differs.
- [Eclipse-kuksa python SDK](https://github.com/eclipse-kuksa/kuksa-python-sdk)
- [Eclipse-kuksa python examples](https://github.com/eclipse-kuksa/kuksa-python-sdk/tree/main/docs/examples)
