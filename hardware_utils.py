import wmi
import subprocess


def check_cpu_usage(device_name):
    """
    Überprüft die CPU-Auslastung eines Geräts.

    Args:
        device_name (str): Der Name des Geräts.

    Returns:
        int: Die CPU-Auslastung in Prozent.
    """
    wmi_obj = wmi.WMI(server=device_name)
    cpu_load = wmi_obj.Win32_Processor()[0].LoadPercentage
    return cpu_load


def check_memory_usage(device_name):
    """
    Überprüft die Speicherauslastung eines Geräts.

    Args:
        device_name (str): Der Name des Geräts.

    Returns:
        float: Die Speicherauslastung in GB.
    """
    wmi_obj = wmi.WMI(server=device_name)
    total_memory = int(wmi_obj.Win32_ComputerSystem()[0].TotalPhysicalMemory) / (1024 ** 3)
    free_memory = int(wmi_obj.Win32_OperatingSystem()[0].FreePhysicalMemory) / (1024 ** 3)
    used_memory = total_memory - free_memory
    return used_memory


def check_disk_usage(device_name):
    """
    Überprüft die Festplattenauslastung eines Geräts.

    Args:
        device_name (str): Der Name des Geräts.

    Returns:
        float: Die Festplattenauslastung in GB.
    """
    wmi_obj = wmi.WMI(server=device_name)
    disk = wmi_obj.Win32_LogicalDisk(DeviceID='C:')
    total_disk_space = int(disk[0].Size) / (1024 ** 3)
    free_disk_space = int(disk[0].FreeSpace) / (1024 ** 3)
    used_disk_space = total_disk_space - free_disk_space
    return used_disk_space


def check_network_availability(device_name):
    """
    Überprüft die Netzwerkverfügbarkeit eines Geräts.

    Args:
        device_name (str): Der Name des Geräts.

    Returns:
        bool: True, wenn das Netzwerk verfügbar ist, sonst False.
    """
    wmi_obj = wmi.WMI(server=device_name)
    network_interface = wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    if len(network_interface) > 0:
        return True
    else:
        return False


def check_network_latency(device_name):
    """
    Überprüft die Netzwerklatenz zu einem Gerät.

    Args:
        device_name (str): Der Name des Geräts.

    Returns:
        float: Die Netzwerklatenz in ms.
    """
    command = f"ping {device_name} -n 4"
    output = subprocess.getoutput(command)
    lines = output.splitlines()
    for line in lines:
        if "Minimum" in line:
            start_index = line.find("=") + 1
            end_index = line.find("ms")
            latency = float(line[start_index:end_index].strip())
            return latency
    return None


def check_service_availability(device_name, service_names):
    """
    Überprüft die Verfügbarkeit von Diensten auf einem Gerät.

    Args:
        device_name (str): Der Name des Geräts.
        service_names (str): Die Namen der Dienste, durch Kommas getrennt.

    Returns:
        bool: True, wenn alle Dienste verfügbar sind, sonst False.
    """
    wmi_obj = wmi.WMI(server=device_name)
    services = wmi_obj.Win32_Service()
    available_services = [service.Name for service in services if service.State == "Running"]

    if ',' in service_names:
        # Mehrere Dienste überprüfen
        services_to_check = [service.strip() for service in service_names.split(',')]
        for service_name in services_to_check:
            if service_name not in available_services:
                return False
    else:
        # Einzelnen Dienst überprüfen
        if service_names.strip() not in available_services:
            return False

    return True



