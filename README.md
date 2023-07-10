# Device Monitoring System

This project is a system for monitoring devices in a network. It captures various hardware metrics such as CPU usage, memory usage, disk usage, network availability and latency, and service availability. It integrates with Jira to create tickets for deviations.

## Technical Implementation

The system consists of several modules:

- Database connection: The module `db_utils.py` establishes a connection to the MySQL database and executes SQL queries to retrieve device data.
- Hardware monitoring: The module `hardware_utils.py` uses the `wmi` library to obtain information about the hardware of the devices. It also uses the `ping` command to measure network latency.
- Jira integration: The module `jira_utils.py` implements the necessary configurations and the function `create_jira_ticket` to create a Jira ticket for a deviating device. The ticket contains detailed information about the detected deviation.
- Device monitoring: The main class `DeviceMonitor` in the module `monitor.py` monitors the devices. It is initialized with the database configuration and has the method `monitor_devices`. This method calls the database function `run_sql_query` to retrieve the device data. Then it uses the hardware monitoring functions to check the current metrics of the devices. In case of deviations, it creates corresponding Jira tickets by calling the function `create_jira_ticket`.

