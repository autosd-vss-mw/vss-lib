+-------------------------------------------------------+
|                   VSS Middleware Layer                |
|         (Manages VSS Operations for All Vendors)      |
+-------------------------------------------------------+
                           |
+-------------------------------------------------------------------+
|                      Vendor-Agnostic VSS Manager                  |
|   (Standardized Operations for Signal Handling, Validation, etc.) |
+-------------------------------------------------------------------+
                           |
                           v
+------------------------+  +------------------------+  +------------------------+
|      Vendor A (Honda)  |  |      Vendor B (Nissan) |  |     Vendor C (Renesas) |
|      VSS Operations    |  |      VSS Operations    |  |      VSS Operations    |
+------------------------+  +------------------------+  +------------------------+
        |                            |                            |
        v                            v                            v
+------------------+       +------------------+       +------------------+
|  Honda VSS File  |       |  Nissan VSS File |       |  Renesas VSS File|
|    (YAML)        |       |    (YAML)        |       |    (YAML)        |
+------------------+       +------------------+       +------------------+
        |                            |                            |
        v                            v                            v
+-------------------------------------------------------------------+
|   VSS D-Bus Interface (optional system interface)                 |
|     (Common Signal Flow for Real-Time & Simulated Communication)  |
+-------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------+  +-------------------------------+
|  Application Layer             |  |  Testing/Simulation Tools     |
|  (ECU, Sensors, etc.)          |  |  (Generate Simulated Signals) |
+--------------------------------+  +-------------------------------+


