from jira import JIRA


username = 'username'
password = 'password'
server = 'https://example.atlassian.net'


def create_jira_ticket(device_name, message):
    """
    Erstellt ein JIRA-Ticket für ein Gerät.

    Args:
        device_name (str): Der Name des Geräts.
        message (str): Die Beschreibung des Fehlers.
    """
    issue_dict = {
        'project': {'key': 'UTL'},
        'summary': f'Fehler bei {device_name}',
        'description': message,
        'issuetype': {'name': 'Bug'},
    }
    jira = JIRA(server=server, basic_auth=(username,password))
    jira.create_issue(fields=issue_dict)
