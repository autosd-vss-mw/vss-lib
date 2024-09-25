// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <iostream>
#include <dbus/dbus.h>
#include <cstdlib>

// Function to send hardware signal to the D-Bus service
void send_hardware_signal(const std::string& signal_name, int value) {
    DBusError err;
    DBusConnection* conn;
    DBusMessage* msg;
    DBusMessageIter args;
    DBusPendingCall* pending;

    // Initialize D-Bus error
    dbus_error_init(&err);

    // Connect to the system D-Bus
    conn = dbus_bus_get(DBUS_BUS_SYSTEM, &err);
    if (dbus_error_is_set(&err)) {
        std::cerr << "Connection Error: " << err.message << std::endl;
        dbus_error_free(&err);
        exit(1);
    }

    if (!conn) {
        std::cerr << "Failed to connect to the D-Bus daemon." << std::endl;
        exit(1);
    }

    // Create a new method call and check for errors
    msg = dbus_message_new_method_call("com.vss_lib.VehicleSignals",  // target service
                                       "/com/vss_lib/VehicleSignals", // object to call on
                                       "com.vss_lib.VehicleSignals",  // interface to call on
                                       "EmitHardwareSignal");         // method name
    if (!msg) {
        std::cerr << "Message Null" << std::endl;
        exit(1);
    }

    // Append arguments
    dbus_message_iter_init_append(msg, &args);
    const char* signal_name_cstr = signal_name.c_str();
    if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &signal_name_cstr)) {
        std::cerr << "Out of Memory!" << std::endl;
        exit(1);
    }
    if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_INT32, &value)) {
        std::cerr << "Out of Memory!" << std::endl;
        exit(1);
    }

    // Send message and get a handle for the reply
    if (!dbus_connection_send_with_reply(conn, msg, &pending, -1)) {
        std::cerr << "Out of Memory!" << std::endl;
        exit(1);
    }

    if (!pending) {
        std::cerr << "Pending Call Null" << std::endl;
        exit(1);
    }

    dbus_connection_flush(conn);
    dbus_message_unref(msg);

    // Block until we receive a reply
    dbus_pending_call_block(pending);

    // Get the reply message
    msg = dbus_pending_call_steal_reply(pending);
    if (!msg) {
        std::cerr << "Reply Null" << std::endl;
        exit(1);
    }

    dbus_pending_call_unref(pending);

    // Free the reply message
    dbus_message_unref(msg);

    std::cout << "Hardware signal '" << signal_name << "' with value " << value << " sent to D-Bus." << std::endl;
}

int main() {
    try {
        send_hardware_signal("Speed", 80);
    } catch (const std::exception& e) {
        std::cerr << "An unexpected error occurred while sending the signal." << std::endl;
        std::cerr << "Details: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
