import docker

# Create docker client
docker_client = docker.from_env()


def list_containers():
    """
    Return list of running containers.
    """
    return docker_client.containers.list()


def get_container_logs(container_name: str, lines: int):
    """
    Get logs from a container.
    """
    container = docker_client.containers.get(container_name)
    return container.logs(tail=lines)


def get_container_status(container_name: str):
    """
    Return container status information.
    """
    container = docker_client.containers.get(container_name)
    return container.status
