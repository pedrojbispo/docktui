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
