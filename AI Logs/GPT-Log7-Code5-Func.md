Prompt:Vamos agora implementar Start e Stop e Restart dos containers, eu quero um submenu para fazer isso
CHATGPT:
Boa 😎 agora estamos mesmo a transformar isto num mini-orchestrator.

Vamos fazer isto bem estruturado:

🎯 Objetivo
Criar um **submenu no TUI** para:

* Start container
* Stop container
* Restart container
* Voltar atrás

E manter a arquitetura limpa:

```
TUI → clicommands → api → server → docker_service
```

---

# 🔵 1️⃣ SERVIDOR

Vamos usar o **Docker SDK**, nada de subprocess aqui 👌

---

## 📄 docker_service.py

Adicionar:

```python
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
```

---

## 📄 server.py

Importar:

```python
from docker_service import start_container, stop_container, restart_container
```

Adicionar endpoints:

```python
@app.route("/container/<container_name>/start", methods=["POST"])
def start(container_name):
    result = start_container(container_name)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/container/<container_name>/stop", methods=["POST"])
def stop(container_name):
    result = stop_container(container_name)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/container/<container_name>/restart", methods=["POST"])
def restart(container_name):
    result = restart_container(container_name)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200
```

---

# 🔵 2️⃣ CLIENTE – API

## 📄 api.py

Adicionar:

```python
def start_container(container_name: str):
    """
    Send start container request.
    """
    return requests.post(f"{SERVER_URL}/container/{container_name}/start")


def stop_container(container_name: str):
    """
    Send stop container request.
    """
    return requests.post(f"{SERVER_URL}/container/{container_name}/stop")


def restart_container(container_name: str):
    """
    Send restart container request.
    """
    return requests.post(f"{SERVER_URL}/container/{container_name}/restart")
```

---

# 🔵 3️⃣ CLIENTE – CLI

## 📄 clicommands.py

Importar:

```python
from api import start_container, stop_container, restart_container
```

Adicionar:

```python
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
```

---

# 🔵 4️⃣ TUI – Submenu de Containers

Agora a parte que queres 👇

## 📄 tui.py

Importar:

```python
from clicommands import (
    command_start,
    command_stop,
    command_restart,
    command_status
)
```

---

## 🧭 Criar submenu

```python
def container_management_menu():
    """
    Submenu for container management.
    """

    while True:
        print("\n--- Container Management ---")
        print("1 - Start container")
        print("2 - Stop container")
        print("3 - Restart container")
        print("4 - List running containers")
        print("5 - Back\n")

        option = input("Select option: ")

        if option == "1":
            container_name = input("Container name: ")
            command_start(container_name)

        elif option == "2":
            container_name = input("Container name: ")
            command_stop(container_name)

        elif option == "3":
            container_name = input("Container name: ")
            command_restart(container_name)

        elif option == "4":
            command_status()

        elif option == "5":
            break

        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")
```

---

## 🔧 Adicionar ao menu principal

No `show_menu()` adiciona:

```
5 - Container management
6 - Exit
```

E no `main_loop()`:

```python
elif option == "5":
    container_management_menu()

elif option == "6":
    print("Exiting...")
    break
```

---

# 🚀 Resultado Final

Agora o fluxo fica assim:

```
dockcli tui
↓
Container Management
↓
Start / Stop / Restart
↓
Voltar
```

Arquitetura limpa ✔
Docker SDK usado corretamente ✔
Separação clara ✔
Submenu funcional ✔

---

# 🔥 Próximo nível possível

Agora podemos:

* 📊 Mostrar estado do container antes de permitir start/stop
* 🧠 Impedir start se já estiver running
* 📈 Mostrar CPU e RAM no submenu
* 🎨 Melhorar visual com Rich
* 🔐 Associar containers a projetos

Qual queres atacar agora? 😎
