import pymysql


def run_sql_query(db_config):
    """
    Führt eine SQL-Abfrage auf der Datenbank aus.

    Args:
        db_config (dict): Die Konfiguration der Datenbankverbindung.

    Returns:
        list: Eine Liste mit den Ergebnissen der SQL-Abfrage.
    """
    query = """
        SELECT device_name, cpu_threshold, memory_threshold, disk_threshold, 
            latency_threshold, bandwidth_threshold, service_names
        FROM devices
    """
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()
