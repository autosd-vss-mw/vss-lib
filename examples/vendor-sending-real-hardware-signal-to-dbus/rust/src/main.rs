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

use dbus::blocking::Connection;
use std::error::Error;
use std::time::Duration;

/// Sends a hardware signal to the D-Bus service.
///
/// # Arguments
/// * `signal_name` - The name of the signal (e.g., "Speed").
/// * `value` - The value of the signal (e.g., 80 for speed).
fn send_hardware_signal(signal_name: &str, value: f64) -> Result<(), Box<dyn Error>> {
    // Connect to the D-Bus system bus
    let conn = Connection::new_system()?;

    // Proxy object for the D-Bus service
    let proxy = conn.with_proxy(
        "com.vss_lib.VehicleSignals",       // Service name
        "/com/vss_lib/VehicleSignals",      // Object path
        Duration::from_millis(5000),        // Timeout duration
    );

    // Call the method EmitHardwareSignal with arguments
    let result: Result<(), dbus::Error> = proxy.method_call(
        "com.vss_lib.VehicleSignals",       // Interface name
        "EmitHardwareSignal",               // Method name
        (signal_name, value),               // Arguments
    );

    match result {
        Ok(_) => {
            println!("Hardware signal '{}' with value {} sent to D-Bus.", signal_name, value);
            Ok(())
        }
        Err(e) => {
            eprintln!("Error: Failed to send the D-Bus message. Details: {}", e);
            Err(Box::new(e))
        }
    }
}

fn main() {
    // Example: Sending real-time speed signal from hardware
    match send_hardware_signal("Speed", 80.0) {
        Ok(_) => println!("Signal sent successfully."),
        Err(e) => eprintln!("Error: Could not send the signal. Details: {}", e),
    }
}
