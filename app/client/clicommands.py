from api import create_project, modify_project, delete_project, get_status, get_allstatus, get_logs, get_projects


def command_create(project_name: str, compose_source: str):
    """
    CLI create command.
    """

    response = create_project(project_name, compose_source)
    print(response.json())

def command_modify(project_name: str, compose_source: str):
    """
    CLI modify command.
    """

    response = modify_project(project_name, compose_source)

    if response.status_code != 200:
        print("Error:", response.json())
    else:
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

def command_allstatus():
    """
    CLI status command.
    """

    response = get_allstatus()
    print(response.json())

def command_logs(container_name: str, lines: int):
    """
    CLI logs command.
    """

    response = get_logs(container_name, lines)
    print(response.text)

def command_list_projects():
    """
    CLI list projects command.
    """

    response = get_projects()

    if response.status_code != 200:
        print("Error retrieving projects")
        return

    projects = response.json()

    if not projects:
        print("No projects found.")
        return

    print("\nExisting projects:")
    for index, project in enumerate(projects):
        print(f"{index + 1} - {project}")
