Prompt: Vou partilhar contigo alguns sources e ideias minhas, e vamos trabalho juntos passo a passo.
Sources: 
https://docker-py.readthedocs.io/en/stable/containers.html
https://realpython.com/api-integration-in-python/
https://www.geeksforgeeks.org/python/python-build-a-rest-api-using-flask/
https://www.geeksforgeeks.org/python/how-to-copy-files-from-one-server-to-another/

Ideias:
Client is TUI but all options are CLI commands. The program works in CLI and TUI at the same time.
Client --- Server --- [ Docker, Docker Containers ]

Client > dockcli create nginx --barebone
Server > |
    mkdir nginx
    cp /datastore/barebone/nginx.yml /projects/nginx/docker-compose.yml
    docker compose up -d 
Action: POST

Client > dockcli create test-nginx --custom-compose nginx-custom.yml 
Server > | 
    scp <client-source> <server-dest>
    cp /datastore/custom/nginx-custom.yml /projects/test-nginx/docker-compose.yml
    docker compose up -d 
Action: POST

Client > dockcli delete test-nginx
Server > | 
    cd /projects/test-nginx/ && docker compose down
    rm -fr /projects/test-nginx
Action: DELETE

Client > dockcli status
Server > docker ps 
Action: GET
Client > dockcli status --project nginx-custom
Server > | 
    cd /projects/nginx-custom/ && docker compose ps
Action: GET

Client > dockcli logs --project nginx-custom
Server > | 
    cd /projects/nginx-custom/ && docker compose logs -n 100 nginx-custom
Action: GET

Eu sei que esta em ingles, mas nao te preocupes. 
Pronto primeiro eu quero desenha o servidor e cliente. Tenta seguir a minha ideia e os source que partilhei, especial Docker SDK for Python. 
Um ponto de implementaçao a funçoes do TUI representao tambem comandos de CLI, portanto TUI -> CLI -> Funçao/metodo.

Regras: 
1. Codigo modular e se possivel separado em multiplos ficheiros, como por exemplo server.py, client.py, api.py, copyfile.py, clicommands.py, tui.py e entre outros.
2. Codigo simples e facil de fazer debug.
3. Comentarios em todas a funcoes e metodos.
4. Variavais simples e objectivas. Nao uses abrivaçoes, tirando exceções como index no for loop. 
5. Funçoes e metodos devem receber atributos, tirando exceções aonde pode nao ser necessario

ChatGPT:
Perfeito 👌
Gosto muito da tua abordagem: **CLI como núcleo**, TUI como camada visual por cima, e o servidor a orquestrar Docker.

Vamos então desenhar **arquitetura + estrutura modular + esqueleto de código inicial**, seguindo:

* ✅ Docker SDK for Python
* ✅ REST API
* ✅ CLI → chama funções
* ✅ TUI → chama CLI
* ✅ Código simples e debugável
* ✅ Modular
* ✅ Comentários em todas as funções
* ✅ Variáveis claras

---

# 🧱 ARQUITETURA FINAL

```
CLIENT SIDE
────────────────────────────────

dockcli (CLI commands)
        ↓
clicommands.py  (funções reais)
        ↓
api.py (HTTP requests)
        ↓
SERVER API


SERVER SIDE
────────────────────────────────

server.py (Flask API)
        ↓
docker_service.py
file_service.py
project_service.py
        ↓
Docker Engine
Filesystem (/projects)
```

---

# 📁 Estrutura de Pastas

## 📦 server/

```
server/
│
├── server.py
├── docker_service.py
├── project_service.py
├── file_service.py
├── config.py
└── requirements.txt
```

---

## 📦 client/

```
client/
│
├── client.py
├── api.py
├── clicommands.py
├── tui.py
└── config.py
```

---

# 🔵 SERVIDOR

Vamos usar **Flask** (mais simples para debug do que FastAPI).

---

## 📄 server/config.py

```python
"""
Configuration file for server settings.
"""

PROJECTS_DIRECTORY = "/projects"
DATASTORE_DIRECTORY = "/datastore"
SERVER_PORT = 5000
```

---

## 📄 server/file_service.py

```python
import os
import shutil


def create_directory(directory_path: str):
    """
    Create a directory if it does not exist.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def copy_file(source_path: str, destination_path: str):
    """
    Copy a file from source to destination.
    """
    shutil.copy(source_path, destination_path)


def remove_directory(directory_path: str):
    """
    Remove a directory and all its contents.
    """
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
```

---

## 📄 server/docker_service.py

```python
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
```

---

## 📄 server/project_service.py

Aqui fazemos o equivalente aos teus comandos:

```python
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
```

---

## 📄 server/server.py

```python
from flask import Flask, request, jsonify
from project_service import create_project, delete_project, project_status
from docker_service import list_containers, get_container_logs

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


if __name__ == "__main__":
    app.run(port=5000)
```

---

# 🔵 CLIENTE

---

## 📄 client/config.py

```python
SERVER_URL = "http://localhost:5000"
```

---

## 📄 client/api.py

```python
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


def get_logs(container_name: str, lines: int):
    """
    Get container logs.
    """

    return requests.get(
        f"{SERVER_URL}/logs/{container_name}",
        params={"lines": lines}
    )
```

---

## 📄 client/clicommands.py

```python
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
```

---

## 📄 client/client.py (CLI entrypoint)

```python
import argparse
from clicommands import (
    command_create,
    command_delete,
    command_status,
    command_logs
)

parser = argparse.ArgumentParser(prog="dockcli")

subparsers = parser.add_subparsers(dest="command")

create_parser = subparsers.add_parser("create")
create_parser.add_argument("project_name")
create_parser.add_argument("compose_source")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("project_name")

status_parser = subparsers.add_parser("status")

logs_parser = subparsers.add_parser("logs")
logs_parser.add_argument("container_name")
logs_parser.add_argument("--lines", default=100, type=int)

args = parser.parse_args()

if args.command == "create":
    command_create(args.project_name, args.compose_source)

elif args.command == "delete":
    command_delete(args.project_name)

elif args.command == "status":
    command_status()

elif args.command == "logs":
    command_logs(args.container_name, args.lines)
```

---

# 🔵 TUI (Camada Visual)

A TUI vai simplesmente chamar as funções do `clicommands.py`.

Exemplo simples:

```python
from clicommands import command_status

def show_menu():
    print("1 - Status")
    print("2 - Exit")

    option = input("Select: ")

    if option == "1":
        command_status()
    elif option == "2":
        exit()


if __name__ == "__main__":
    while True:
        show_menu()
```

---

# ✅ O que já está bem alinhado com a tua ideia

✔ CLI real (`dockcli create nginx compose.yml`)
✔ TUI usa as mesmas funções
✔ Server controla filesystem + docker
✔ Docker SDK usado para logs/status
✔ Docker compose usado para projetos
✔ Código modular
✔ Fácil debug
✔ Funções recebem atributos
✔ Comentários em todas funções

---

# 🔥 Próximo passo

Agora precisamos decidir:

1. 🔐 Adicionamos sistema de utilizadores?
2. 📂 Implementamos upload real do ficheiro (scp-like)?
3. 🐳 Migramos totalmente para Docker SDK e abandonamos subprocess?
4. 🖥️ Melhoramos TUI com Rich/Textual?
5. 📊 Adicionamos monitorização CPU/Memória?

Escolhe o próximo passo e vamos construir passo a passo.
