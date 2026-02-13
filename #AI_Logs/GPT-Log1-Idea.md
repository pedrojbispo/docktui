Prompt: 
Criar uma aplicação em Python que gere um servidor Docker. 
Existem 2 componentes, um cliente, feito em terminal ou TUI (Terminal User Interface) e 
um servidor com uma API que controla os containers Docker. 
O servidor controla os containers, pode instalar, configurar, ligar, desligar, reiniciar, 
remover o container. Pode adicionalmente também provisionar o container com software, 
tipo uma app através de uma script de instalação criada pelo utilizador.
Em termos de dados, existe uma base de dados para contas de utilizadores e servidores. 
O objetivo é ter um sistema de utilizadores, em que cada container criado é referenciado 
pelo utilizador.
O cliente TUI (Terminal User Interface) é a interface no terminal que permite gerir os 
containers no servidor, ou seja, criar, remover, modificar instâncias e também monitorizar 
o container em termos de status e recursos em utilização

ChatGPT:

Boa ideia de projeto — isto dá **um mini-PaaS em Python** 👌
Vou estruturar a resposta em **arquitetura + tecnologias + componentes + exemplo de implementação base** (com código simples para arrancares).

---

## 1️⃣ Arquitetura Geral

```
┌────────────┐        HTTP / REST        ┌────────────────────┐
│ Cliente    │  ─────────────────────▶  │ Servidor API       │
│ TUI        │                           │ (FastAPI)          │
│ (Terminal) │  ◀─────────────────────  │                    │
└────────────┘        JSON               │  Docker SDK        │
                                         │  Base de Dados     │
                                         └─────────┬─────────┘
                                                   │
                                             Docker Engine
                                                   │
                                           Containers
```

---

## 2️⃣ Tecnologias sugeridas

### Servidor

* **Python 3.10+**
* **FastAPI** → API REST
* **Docker SDK for Python** (`docker`)
* **Base de dados**:

  * SQLite (simples) ou
  * PostgreSQL (mais realista)
* **ORM**: SQLAlchemy
* **Auth**: JWT (login/token)

### Cliente (TUI)

* **Rich** ou **Textual**
* Comunicação via **HTTP (requests)**

---

## 3️⃣ Funcionalidades por componente

## 🔹 Servidor (API)

### Containers

* Criar container
* Ligar / desligar
* Reiniciar
* Remover
* Provisionar software via **script bash**
* Monitorizar:

  * Estado
  * CPU
  * Memória

### Utilizadores

* Criar conta
* Login
* Cada container pertence a **1 utilizador**

---

## 4️⃣ Modelo de Dados (simplificado)

### User

```text
id
username
password_hash
```

### Container

```text
id
docker_id
name
image
user_id
status
created_at
```

---

## 5️⃣ Servidor – Estrutura de pastas

```
server/
├── main.py
├── database.py
├── models.py
├── auth.py
├── docker_service.py
└── requirements.txt
```

---

## 6️⃣ Servidor – Código base

### `requirements.txt`

```txt
fastapi
uvicorn
docker
sqlalchemy
passlib[bcrypt]
python-jose
```

---

### `docker_service.py`

```python
import docker

client = docker.from_env()

def create_container(image, name, command=None):
    container = client.containers.run(
        image,
        command=command,
        name=name,
        detach=True
    )
    return container.id

def stop_container(container_id):
    client.containers.get(container_id).stop()

def start_container(container_id):
    client.containers.get(container_id).start()

def remove_container(container_id):
    client.containers.get(container_id).remove(force=True)

def stats_container(container_id):
    container = client.containers.get(container_id)
    return container.stats(stream=False)
```

---

### `main.py`

```python
from fastapi import FastAPI
from docker_service import *

app = FastAPI()

@app.post("/containers/")
def create(image: str, name: str):
    cid = create_container(image, name)
    return {"container_id": cid}

@app.post("/containers/{container_id}/start")
def start(container_id: str):
    start_container(container_id)
    return {"status": "started"}

@app.post("/containers/{container_id}/stop")
def stop(container_id: str):
    stop_container(container_id)
    return {"status": "stopped"}

@app.delete("/containers/{container_id}")
def remove(container_id: str):
    remove_container(container_id)
    return {"status": "removed"}

@app.get("/containers/{container_id}/stats")
def stats(container_id: str):
    return stats_container(container_id)
```

Executar:

```bash
uvicorn main:app --reload
```

---

## 7️⃣ Provisionamento de software (script)

Exemplo:

```bash
#!/bin/bash
apt update
apt install -y nginx
```

Python:

```python
def provision(container_id, script_path):
    container = client.containers.get(container_id)
    with open(script_path) as f:
        script = f.read()
    container.exec_run(f"/bin/bash -c '{script}'")
```

---

## 8️⃣ Cliente TUI – Estrutura

```
client/
├── tui.py
└── api.py
```

---

### `api.py`

```python
import requests

API = "http://localhost:8000"

def create_container(image, name):
    return requests.post(
        f"{API}/containers/",
        params={"image": image, "name": name}
    ).json()
```

---

### `tui.py` (exemplo simples)

```python
from rich.console import Console
from api import create_container

console = Console()

console.print("[bold cyan]Docker Manager[/bold cyan]")
image = console.input("Imagem: ")
name = console.input("Nome: ")

result = create_container(image, name)
console.print(result)
```

---

## 9️⃣ Monitorização no TUI

Mostrar:

* Estado
* CPU %
* RAM

Usando `docker stats` via API → JSON → Rich tables.

---

## 🔟 O que este projeto demonstra (para avaliação)

✔ Arquitetura cliente-servidor
✔ API REST
✔ Docker automation
✔ Autenticação
✔ TUI moderna
✔ Separação de responsabilidades
✔ Base para escalar (multi-user)

---

## Queres que eu:

* 📄 transforme isto num **relatório académico formal**
* 🧱 implemente **autenticação JWT**
* 🖥️ faça uma **TUI completa com menus**
* 📊 adicione **monitorização visual**
* 🐳 crie um **docker-compose do sistema**

Diz-me o foco da disciplina e o nível de detalhe que precisas 😉
