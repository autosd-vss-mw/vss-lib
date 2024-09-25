/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package main

import (
	"fmt"
	"github.com/godbus/dbus/v5"
	"log"
)

// sendHardwareSignal sends a hardware signal to the D-Bus service.
//
// signalName: The name of the signal (e.g., "Speed").
// value: The value of the signal (e.g., 80.0 for speed).
func sendHardwareSignal(signalName string, value float64) error {
	// Connect to the system bus
	conn, err := dbus.SystemBus()
	if err != nil {
		return fmt.Errorf("failed to connect to the system bus: %v", err)
	}

	// Object to call the D-Bus method
	obj := conn.Object("com.vss_lib.VehicleSignals", "/com/vss_lib/VehicleSignals")

	// Call the EmitHardwareSignal method with signalName and value
	call := obj.Call("com.vss_lib.VehicleSignals.EmitHardwareSignal", 0, signalName, value)
	if call.Err != nil {
		return fmt.Errorf("failed to send D-Bus message: %v", call.Err)
	}

	fmt.Printf("Hardware signal '%s' with value %f sent to D-Bus.\n", signalName, value)
	return nil
}

func main() {
	// Example: Sending real-time speed signal from hardware
	err := sendHardwareSignal("Speed", 80.0)
	if err != nil {
		log.Fatalf("Error: Could not send the signal. Details: %v", err)
	} else {
		fmt.Println("Signal sent successfully.")
	}
}
