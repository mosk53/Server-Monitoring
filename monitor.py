from db_utils import run_sql_query
from hardware_utils import (
    check_cpu_usage,
    check_memory_usage,
    check_disk_usage,
    check_network_availability,
    check_network_latency,
    check_service_availability,
)
from jira_utils import create_jira_ticket


class DeviceMonitor:
    
    """
    Klasse zur Überwachung von Geräten.
    """

    def __init__(self, db_config):
        """
        Initialisiert eine neue Instanz des DeviceMonitor.

        Args:
            db_config (str): Die Konfiguration für die Datenbankverbindung.
        """
        self.db_config = db_config

    def monitor_devices(self):
        """
        Überwacht die Geräte und erstellt JIRA-Tickets bei Abweichungen.
        """
        device_data = run_sql_query(self.db_config)

        for device in device_data:
            (
                device_name, cpu_threshold, memory_threshold, disk_threshold,
                latency_threshold, service_names
            ) = device

            cpu_usage = check_cpu_usage(device_name)
            memory_usage = check_memory_usage(device_name)
            disk_usage = check_disk_usage(device_name)
            network_available = check_network_availability(device_name)
            network_latency = check_network_latency(device_name)
            service_available = check_service_availability(device_name, service_names)

            if (
                cpu_usage > cpu_threshold or
                memory_usage > memory_threshold or
                disk_usage > disk_threshold or
                not network_available or
                (network_latency is not None and network_latency > latency_threshold) or
                not service_available
            ):
                if cpu_usage > cpu_threshold:
                    create_jira_ticket(
                        device_name,
                        f"Die CPU-Auslastung liegt bei {cpu_usage}%. "
                        f"Der Schwellenwert beträgt {cpu_threshold}%."
                    )
                if memory_usage > memory_threshold:
                    create_jira_ticket(
                        device_name,
                        f"Die Speicherauslastung liegt bei {memory_usage}GB. "
                        f"Der Schwellenwert beträgt {memory_threshold}GB."
                    )
                if disk_usage > disk_threshold:
                    create_jira_ticket(
                        device_name,
                        f"Die Festplattenauslastung liegt bei {disk_usage}GB. "
                        f"Der Schwellenwert beträgt {disk_threshold}GB."
                    )
                if not network_available:
                    create_jira_ticket(device_name, f"Das Netzwerk ist nicht verfügbar.")
                if network_latency is not None and network_latency > latency_threshold:
                    create_jira_ticket(
                        device_name,
                        f"Die Netzwerklatenz liegt bei {network_latency}ms. "
                        f"Der Schwellenwert beträgt {latency_threshold}ms."
                    )
                if not service_available:
                    create_jira_ticket(
                        device_name,
                        f"Service {service_names} ist nicht verfügbar."
                    )
