To start the program, it can be done by:
python tui.py

Or

python client tui

The client.py commands:

python client tui > To launch the TUI

python client create <project_name> <compose_source>  -> To create a project

python client modify <project_name> <compose_source>  -> To modify a project

python client delete <project_name>  -> To delete a project

python client logs <project_name> <num_of_lines>  -> To display project container logs

python client status -> To display running containers

python client allstatus -> To display all containers regardless the state

python client projects -> To list projects

python client start -> To start a container

python client stop -> To stop a container

python client restart -> To restart a container
