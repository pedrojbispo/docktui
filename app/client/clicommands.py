from api import create_project, delete_project, get_status, get_logs


def command_create(project_name: str, compose_source: str):
    """
    CLI create command.
    """

    response = create_project(project_name, compose_source)
    print(response.json())


def command_delete(project_name: str):
    """
    CLI delete command.
    """

    response = delete_project(project_name)
    print(response.json())


def command_status():
    """
    CLI status command.
    """

    response = get_status()
    print(response.json())


def command_logs(container_name: str, lines: int):
    """
    CLI logs command.
    """

    response = get_logs(container_name, lines)
    print(response.text)
