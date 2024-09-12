#!/usr/bin/env python3
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

import argparse
from pydbus import SystemBus


def main():
    parser = argparse.ArgumentParser(description="VSS D-Bus Client to send signals.")
    parser.add_argument("--vendor", help="Specify the vendor (e.g., toyota, bmw, renesas)")
    args = parser.parse_args()

    if not args.vendor:
        print("Vendor must be specified!")
        return

    bus = SystemBus()
    vss_service = bus.get("com.vss_lib.VehicleSignals")

    # Example: Sending a speed signal for the specified vendor
    signal_name = "Speed"
    value = 100  # Example speed value
    vss_service.EmitHardwareSignal(signal_name, value)
    print(f"Signal '{signal_name}' with value {value} sent by {args.vendor}.")


if __name__ == "__main__":
    main()
