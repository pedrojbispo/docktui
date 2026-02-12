import requests
from config import SERVER_URL


def create_project(project_name: str, compose_source: str):
    """
    Send request to create project.
    """

    payload = {
        "project_name": project_name,
        "compose_source": compose_source
    }

    return requests.post(f"{SERVER_URL}/create", json=payload)

def modify_project(project_name: str, compose_source: str):
    """
    Send request to modify project.
    """

    payload = {
        "project_name": project_name,
        "compose_source": compose_source
    }

    return requests.post(f"{SERVER_URL}/modify", json=payload)

def delete_project(project_name: str):
    """
    Send delete request.
    """

    return requests.delete(f"{SERVER_URL}/delete/{project_name}")


def get_status():
    """
    Get running containers.
    """

    return requests.get(f"{SERVER_URL}/status")

def get_allstatus():
    """
    Get all containers.
    """

    return requests.get(f"{SERVER_URL}/allstatus")

def get_logs(container_name: str, lines: int):
    """
    Get container logs.
    """

    return requests.get(
        f"{SERVER_URL}/logs/{container_name}",
        params={"lines": lines}
    )

def get_projects():
    """
    Get list of projects from server.
    """

    return requests.get(f"{SERVER_URL}/projects")