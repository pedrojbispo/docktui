"""Module providing server APP."""

from flask import Flask, request, jsonify
from project_service import (
    create_project,
    modify_project,
    delete_project,
    list_projects
)
from docker_service import (
    list_containers,
    list_allcontainers,
    get_container_logs,
    start_container,
    stop_container,
    restart_container
)

app = Flask(__name__)


@app.route("/create", methods=["POST"])
def create():
    """
    Create a new docker project.
    """

    data = request.json
    project_name = data.get("project_name")
    compose_source = data.get("compose_source")

    result = create_project(project_name, compose_source)
    return jsonify(result)

@app.route("/modify", methods=["POST"])
def modify():
    """
    Modify a new docker project.
    """

    data = request.json
    project_name = data.get("project_name")
    compose_source = data.get("compose_source")

    result = modify_project(project_name, compose_source)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/delete/<project_name>", methods=["DELETE"])
def delete(project_name):
    """
    Delete docker project.
    """

    result = delete_project(project_name)
    return jsonify(result)


@app.route("/status", methods=["GET"])
def status():
    """
    List running containers.
    """

    containers = list_containers()
    container_names = [container.name for container in containers]

    return jsonify(container_names)

@app.route("/logs/<container_name>", methods=["GET"])
def logs(container_name):
    """
    Return logs of a container.
    """

    lines = request.args.get("lines", default=100, type=int)
    logs_output = get_container_logs(container_name, lines)

    return logs_output.decode("utf-8")

@app.route("/allstatus", methods=["GET"])
def allstatus():
    """
    List all containers.
    """

    containers = list_allcontainers()
    container_names = [container.name for container in containers]

    return jsonify(container_names)

@app.route("/projects", methods=["GET"])
def projects():
    """
    Return list of existing projects.
    """

    project_list = list_projects()
    return jsonify(project_list)

@app.route("/container/<container_name>/start", methods=["POST"])
def start(container_name):
    """
    Start Container.
    """
    result = start_container(container_name)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/container/<container_name>/stop", methods=["POST"])
def stop(container_name):
    """
    Stop Container.
    """
    result = stop_container(container_name)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/container/<container_name>/restart", methods=["POST"])
def restart(container_name):
    """
    Restart Container.
    """
    result = restart_container(container_name)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(port=5000)
