import docker

# Create docker client
docker_client = docker.from_env()


def list_containers():
    """
    Return list of running containers.
    """
    return docker_client.containers.list()

def list_allcontainers():
    """
    Return list of running containers.
    """
    return docker_client.containers.list(all)

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

def start_container(container_name: str):
    """
    Start a stopped container.
    """
    try:
        container = docker_client.containers.get(container_name)
        container.start()
        return {"status": "started", "container": container_name}
    except Exception as error:
        return {"error": str(error)}


def stop_container(container_name: str):
    """
    Stop a running container.
    """
    try:
        container = docker_client.containers.get(container_name)
        container.stop()
        return {"status": "stopped", "container": container_name}
    except Exception as error:
        return {"error": str(error)}


def restart_container(container_name: str):
    """
    Restart a container.
    """
    try:
        container = docker_client.containers.get(container_name)
        container.restart()
        return {"status": "restarted", "container": container_name}
    except Exception as error:
        return {"error": str(error)}