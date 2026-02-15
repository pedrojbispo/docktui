To start the program, it can be done by:
python tui.py

Or

python client.py tui

The client.py.py commands:

python client.py tui > To launch the TUI

python client.py create <project_name> <compose_source>  -> To create a project

python client.py modify <project_name> <compose_source>  -> To modify a project

python client.py delete <project_name>  -> To delete a project

python client.py logs <project_name> <num_of_lines>  -> To display project container logs

python client.py status -> To display running containers

python client.py allstatus -> To display all containers regardless the state

python client.py projects -> To list projects

python client.py start -> To start a container

python client.py stop -> To stop a container

python client.py restart -> To restart a container
