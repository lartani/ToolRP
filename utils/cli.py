import os
from .config import versions
from .core.models import add_new_model
from .core.packs import (
    ensure_required_directories,
    create_resource_pack,
    choose_resource_pack,
    choose_namespace,
    export_pack,
)


def edit_resource_pack():
    selected_pack = choose_resource_pack()
    if selected_pack:
        # Placeholder for editing logic
        print(f"Editing resource pack: {selected_pack.name}")
        namespace = choose_namespace(selected_pack)
        if not namespace:
            print("No namespace selected. Exiting edit mode.")
            return None

        add_new_model(namespace, selected_pack)


def print_options(options):
    for key, value in options.items():
        print(f"{key}. {value[0]}")


def create_pack_menu():
    name = input("Enter the name of the new resource pack: ")
    for ver in versions.keys():
        print(f"- {ver}")
    version = input("Enter the Minecraft version (or leave blank for default): ")
    if not version:
        version = None  # Default to the latest version if no input is provided

    try: 
        return create_resource_pack(name, version)
    except (FileExistsError, ValueError) as e:
        print(e)


def run_menu(options):
    print_options(options)
    while True:
        try:
            choice: int = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice in options.keys():
            if options[choice][1] is None:
                print("Bye!")
                break
            options[choice][1]()
            print_options(
                options
            )  # Show options again after executing the chosen function
        else:
            print("Invalid choice. Please select a valid option.")


options = {
    1: ("Create a new resource pack", create_pack_menu),
    2: ("Edit an existing resource pack", edit_resource_pack),
    3: ("Export a resource pack", lambda: export_pack(choose_resource_pack())),
    4: ("Exit", None),
}

if __name__ == "__main__":
    ensure_required_directories()
    print(
        "Welcome to ToolRP! This is a utility to creating and editing resource packs for Minecraft!"
    )
    try:
        run_menu(options)
    except (KeyboardInterrupt, EOFError):
        print("Bye!")
