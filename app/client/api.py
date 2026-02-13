"""Module providing a API comunication layer to server."""

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

    return requests.post(f"{SERVER_URL}/create", json=payload, timeout=30)

def modify_project(project_name: str, compose_source: str):
    """
    Send request to modify project.
    """

    payload = {
        "project_name": project_name,
        "compose_source": compose_source
    }

    return requests.post(f"{SERVER_URL}/modify", json=payload, timeout=30)

def delete_project(project_name: str):
    """
    Send delete request.
    """

    return requests.delete(f"{SERVER_URL}/delete/{project_name}", timeout=30)


def get_status():
    """
    Get running containers.
    """

    return requests.get(f"{SERVER_URL}/status", timeout=30)

def get_allstatus():
    """
    Get all containers.
    """

    return requests.get(f"{SERVER_URL}/allstatus", timeout=30)

def get_logs(container_name: str, lines: int):
    """
    Get container logs.
    """

    return requests.get(f"{SERVER_URL}/logs/{container_name}",params={"lines": lines}, timeout=30)

def get_projects():
    """
    Get list of projects from server.
    """

    return requests.get(f"{SERVER_URL}/projects", timeout=30)

def start_container(container_name: str):
    """
    Send start container request.
    """
    return requests.post(f"{SERVER_URL}/container/{container_name}/start", timeout=30)


def stop_container(container_name: str):
    """
    Send stop container request.
    """
    return requests.post(f"{SERVER_URL}/container/{container_name}/stop", timeout=30)


def restart_container(container_name: str):
    """
    Send restart container request.
    """
    return requests.post(f"{SERVER_URL}/container/{container_name}/restart", timeout=30)
