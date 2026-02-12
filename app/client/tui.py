"""
Terminal User Interface for dockcli.
This module provides an interactive menu that calls CLI commands.
"""

from clicommands import (
    command_create,
    command_modify,
    command_delete,
    command_status,
    command_allstatus,
    command_logs,
    command_list_projects
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
    print("2 - Modify project")
    print("3 - Delete project")
    print("4 - Status (all running containers)")
    print("5 - Logs")
    print("6 - All status")
    print("0 - Exit\n")


def handle_create():
    """
    Handle create project interaction.
    """
    project_name = input("Project name: ")
    compose_source = input("Path to docker-compose file: ")

    command_create(project_name, compose_source)

def handle_modify():
    """
    Handle modify project interaction.
    """
    
    print("\nAvailable projects:")
    command_list_projects()

    project_name = input("Project name: ")
    compose_source = input("Path to docker-compose file: ")

    command_modify(project_name, compose_source)

def handle_delete():
    """
    Handle delete project interaction.
    """

    print("\nAvailable projects:")
    command_list_projects()

    project_name = input("Project name: ")

    command_delete(project_name)


def handle_status():
    """
    Handle status request.
    """
    command_status()

def handle_allstatus():
    """
    Handle status request.
    """
    command_allstatus()


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
            handle_modify()

        elif option == "3":
            handle_delete()

        elif option == "4":
            handle_status()

        elif option == "5":
            handle_logs()

        elif option == "6":
            handle_allstatus()

        elif option == "0":
            print("Exiting...")
            break

        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_loop()
