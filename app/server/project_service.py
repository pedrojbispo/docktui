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
