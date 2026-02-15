"""Module providing the client APP."""

import argparse
from commands import (
    command_create,
    command_modify,
    command_delete,
    command_status,
    command_allstatus,
    command_logs,
    command_list_projects,
    command_start,
    command_stop,
    command_restart
)


parser = argparse.ArgumentParser(prog="dockcli")

subparsers = parser.add_subparsers(dest="command")

tui_parser = subparsers.add_parser("tui")

create_parser = subparsers.add_parser("create")
create_parser.add_argument("project_name")
create_parser.add_argument("compose_source")

modify_parser = subparsers.add_parser("modify")
modify_parser.add_argument("project_name")
modify_parser.add_argument("compose_source")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("project_name")

status_parser = subparsers.add_parser("status")

logs_parser = subparsers.add_parser("logs")
logs_parser.add_argument("container_name")
logs_parser.add_argument("--lines", default=100, type=int)

project_parser = subparsers.add_parser("projects")

ct_start_parser = subparsers.add_parser("start")
ct_start_parser.add_argument("container_name")

ct_stop_parser = subparsers.add_parser("stop")
ct_stop_parser.add_argument("container_name")

ct_restart_parser = subparsers.add_parser("restart")
ct_restart_parser.add_argument("container_name")

args = parser.parse_args()

if args.command == "create":
    command_create(args.project_name, args.compose_source)

elif args.command == "modify":
    command_modify(args.project_name, args.compose_source)

elif args.command == "delete":
    command_delete(args.project_name)

elif args.command == "status":
    command_status()

elif args.command == "allstatus":
    command_allstatus()

elif args.command == "logs":
    command_logs(args.container_name, args.lines)

elif args.command == "projects":
    command_list_projects()

elif args.command == "start":
    command_start(args.container_name)

elif args.command == "stop":
    command_stop(args.container_name)

elif args.command == "restart":
    command_restart(args.container_name)

elif args.command == "tui":
    from tui import main_loop
    main_loop()
