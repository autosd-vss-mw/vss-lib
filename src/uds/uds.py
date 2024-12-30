import struct
import time

class UDSHandler:
    def __init__(self, transport_layer, config):
        self.transport_layer = transport_layer  # E.g., CAN, TCP
        self.config = config  # Timing, P2CAN, P2StarCAN, etc.

    def send_request(self, service_id, subfunction=None, data=None):
        # Construct UDS request packet
        payload = struct.pack("B", service_id)
        if subfunction:
            payload += struct.pack("B", subfunction)
        if data:
            payload += data

        self.transport_layer.send(payload)
        response = self.transport_layer.receive()
        return self.parse_response(response)

    def parse_response(self, response):
        # Parse UDS response data
        service_id = response[0]
        if service_id & 0x40 == 0x40:  # Positive response
            return {"status": "success", "data": response[1:]}
        else:  # Negative response
            return {"status": "error", "code": response[1]}

    def read_dtc(self):
        # Example: Read DTC Information (0x19 service)
        return self.send_request(0x19, subfunction=0x02)  # Read all DTCs
