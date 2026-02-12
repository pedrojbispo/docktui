Prompt: Vamos melhorar o TUI, neste momento so temos a opçao de status e sai, vamos adicionar as outros 
CHATGPT: 
Boa 😎 agora começamos a entrar na parte divertida.

Neste momento o TUI é basicamente um `print + input`.
Vamos evoluir para algo:

* ✅ Menu completo
* ✅ Separação clara por ações
* ✅ Usa as funções do `clicommands.py`
* ✅ Código simples e debugável
* ✅ Estrutura organizada
* ✅ Fácil de expandir depois

Não vamos ainda usar `Textual`, vamos manter simples e limpo.

---

# 🎯 Objetivo do novo TUI

Menu principal:

```
Docker CLI Manager

1 - Create project
2 - Delete project
3 - Status (all)
4 - Status (project)
5 - Logs
6 - Exit
```

---

# 📄 client/tui.py (versão melhorada)

```python
"""
Terminal User Interface for dockcli.
This module provides an interactive menu that calls CLI commands.
"""

from clicommands import (
    command_create,
    command_delete,
    command_status,
    command_logs
)


def show_header():
    """
    Print application header.
    """
    print("\n==============================")
    print("      DOCKCLI MANAGER")
    print("==============================\n")


def show_menu():
    """
    Print available options.
    """
    print("1 - Create project")
    print("2 - Delete project")
    print("3 - Status (all containers)")
    print("4 - Logs")
    print("5 - Exit\n")


def handle_create():
    """
    Handle create project interaction.
    """
    project_name = input("Project name: ")
    compose_source = input("Path to docker-compose file: ")

    command_create(project_name, compose_source)


def handle_delete():
    """
    Handle delete project interaction.
    """
    project_name = input("Project name: ")

    command_delete(project_name)


def handle_status():
    """
    Handle status request.
    """
    command_status()


def handle_logs():
    """
    Handle logs request.
    """
    container_name = input("Container name: ")
    lines_input = input("Number of log lines (default 100): ")

    if lines_input.strip() == "":
        lines = 100
    else:
        lines = int(lines_input)

    command_logs(container_name, lines)


def main_loop():
    """
    Main interactive loop.
    """
    while True:
        show_header()
        show_menu()

        option = input("Select option: ")

        if option == "1":
            handle_create()

        elif option == "2":
            handle_delete()

        elif option == "3":
            handle_status()

        elif option == "4":
            handle_logs()

        elif option == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_loop()
```

---

# 🔵 Pequena melhoria opcional (boa prática)

No `client.py` podemos permitir:

```
dockcli tui
```

Adicionar isto ao argparse:

```python
tui_parser = subparsers.add_parser("tui")
```

E depois:

```python
elif args.command == "tui":
    from tui import main_loop
    main_loop()
```

Assim temos:

```
dockcli create ...
dockcli delete ...
dockcli status
dockcli logs ...
dockcli tui   ← modo interativo
```

Isso fica muito mais profissional 👌

---

# 🚀 Próximo upgrade possível

Podemos agora:

* ✅ Adicionar "Status por projeto"
* ✅ Adicionar confirmação antes de apagar projeto
* ✅ Melhorar visual com cores (usando Rich)
* ✅ Mostrar output formatado em tabela
* ✅ Mostrar CPU / RAM no status
* ✅ Adicionar barra de progresso

Qual queres fazer a seguir?
Vamos evoluir isto de “projeto académico” para “mini ferramenta real” 😄
