"""Module providing project service."""

import os
import subprocess
from config import PROJECTS_DIRECTORY, DATASTORE_DIRECTORY
from file_service import create_directory, copy_file, remove_directory


def create_project(project_name: str, compose_source: str):
    """
    Create a project directory and start docker compose.
    """

    project_path = os.path.join(PROJECTS_DIRECTORY, project_name)

    create_directory(project_path)

    destination_compose = os.path.join(project_path, "docker-compose.yml")

    copy_file(compose_source, destination_compose)

    subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=project_path
    )

    return {"status": "created", "project": project_name}

def modify_project(project_name: str, compose_source: str):
    """
    Modifies a project directory and start docker compose.
    """

    # Validate input
    if not project_name:
        return {"error": "Project name is required"}

    if not compose_source:
        return {"error": "Compose source path is required"}

    # Prevent path traversal
    if ".." in project_name or "/" in project_name:
        return {"error": "Invalid project name"}

    project_path = os.path.join(PROJECTS_DIRECTORY, project_name)

    # Check if project directory exists
    if not os.path.exists(project_path):
        return {"error": f"Project '{project_name}' does not exist"}

    # Check if compose file exists
    if not os.path.exists(compose_source):
        return {"error": "Compose source file does not exist"}

    destination_compose = os.path.join(project_path, "docker-compose.yml")

    try:
        # Replace docker-compose file
        copy_file(compose_source, destination_compose)

        # Recreate containers
        result = subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=project_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "error": "Docker compose failed",
                "details": result.stderr
            }

        return {
            "status": "modified",
            "project": project_name
        }

    except Exception as error:
        return {
            "error": "Unexpected server error",
            "details": str(error)
        }

def delete_project(project_name: str):
    """
    Stop and remove a docker compose project.
    """

    project_path = os.path.join(PROJECTS_DIRECTORY, project_name)

    subprocess.run(
        ["docker", "compose", "down"],
        cwd=project_path
    )

    remove_directory(project_path)

    return {"status": "deleted", "project": project_name}


def project_status(project_name: str):
    """
    Get docker compose status for a project.
    """

    project_path = os.path.join(PROJECTS_DIRECTORY, project_name)

    result = subprocess.run(
        ["docker", "compose", "ps"],
        cwd=project_path,
        capture_output=True,
        text=True
    )

    return result.stdout

def docker_containers_status():
    """
    Get all docker containers status.
    """

    result = subprocess.run(
        ["docker", "ps", "-a"],
        capture_output=True,
        text=True
    )

    return result.stdout

def list_projects():
    """
    Return a list of existing project directories.
    """

    if not os.path.exists(PROJECTS_DIRECTORY):
        return []

    projects = []

    for name in os.listdir(PROJECTS_DIRECTORY):
        project_path = os.path.join(PROJECTS_DIRECTORY, name)

        if os.path.isdir(project_path):
            projects.append(name)

    return projects
