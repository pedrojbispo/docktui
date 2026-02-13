"""Module providing CLI Commands for the APP."""

from api import (
    create_project,
    modify_project,
    delete_project,
    get_status,
    get_allstatus,
    get_logs,
    get_projects,
    start_container,
    stop_container,
    restart_container
)


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
    CLI all status command.
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

def command_start(container_name: str):
    """
    CLI start container command.
    """
    response = start_container(container_name)

    if response.status_code != 200:
        print("Error:", response.json())
    else:
        print(response.json())


def command_stop(container_name: str):
    """
    CLI stop container command.
    """
    response = stop_container(container_name)

    if response.status_code != 200:
        print("Error:", response.json())
    else:
        print(response.json())


def command_restart(container_name: str):
    """
    CLI restart container command.
    """
    response = restart_container(container_name)

    if response.status_code != 200:
        print("Error:", response.json())
    else:
        print(response.json())
