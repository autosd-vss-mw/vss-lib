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

#include <stdio.h>
#include <stdlib.h>
#include <dbus/dbus.h>

/**
 * Sends a hardware signal to the D-Bus service.
 * 
 * @param signal_name The name of the signal (e.g., "Speed").
 * @param value The value of the signal (e.g., 80 for speed).
 */
void send_hardware_signal(const char* signal_name, int value) {
    DBusConnection* connection;
    DBusError error;
    DBusMessage* msg;
    DBusMessageIter args;
    dbus_error_init(&error);

    // Connect to the system bus
    connection = dbus_bus_get(DBUS_BUS_SYSTEM, &error);
    if (dbus_error_is_set(&error)) {
        fprintf(stderr, "Error: Cannot connect to the system bus. %s\n", error.message);
        dbus_error_free(&error);
        exit(1);
    }

    if (!connection) {
        fprintf(stderr, "Error: Failed to connect to the system bus.\n");
        exit(1);
    }

    // Create a new method call message
    msg = dbus_message_new_method_call("com.vss_lib.VehicleSignals", // Service name
                                       "/com/vss_lib/VehicleSignals", // Object path
                                       "com.vss_lib.VehicleSignals", // Interface name
                                       "EmitHardwareSignal"); // Method name
    if (!msg) {
        fprintf(stderr, "Error: Cannot allocate D-Bus message.\n");
        exit(1);
    }

    // Append arguments to the message
    dbus_message_iter_init_append(msg, &args);
    if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &signal_name) ||
        !dbus_message_iter_append_basic(&args, DBUS_TYPE_INT32, &value)) {
        fprintf(stderr, "Error: Failed to append arguments to D-Bus message.\n");
        exit(1);
    }

    // Send the message and flush the connection
    if (!dbus_connection_send(connection, msg, NULL)) {
        fprintf(stderr, "Error: Failed to send the D-Bus message.\n");
        exit(1);
    }
    dbus_connection_flush(connection);

    printf("Hardware signal '%s' with value %d sent to D-Bus.\n", signal_name, value);

    // Clean up
    dbus_message_unref(msg);
    dbus_connection_unref(connection);
}

int main() {
    const char* signal_name = "Speed";
    int value = 80;

    // Send real-time speed signal from hardware
    send_hardware_signal(signal_name, value);

    return 0;
}
