import os
from pathlib import Path
from .config import versions, RESOURCE_PACKS_DIR, EXPORTED_PACKS_DIR
from .core.models import add_new_model
from .core.packs import (
    ensure_required_directories,
    create_resource_pack,
    get_resource_pack,
    get_namespace,
    export_pack,
)


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

def list_resource_packs():
    packs = [path for path in RESOURCE_PACKS_DIR.iterdir() if path.is_dir()]
    if not packs:
        print("No resource packs found. Please create a new resource pack first.")
        return None
    for pack in packs:
        print(f"- {pack.name}")

def list_namespaces(resource_pack: Path):
    assets_dir = resource_pack / "assets"
    namespaces = [d.name for d in assets_dir.iterdir() if d.is_dir()]
    if not namespaces:
        print(f"No namespaces found in resource pack '{resource_pack.name}'. Please create a new namespace first.")
        return None
    for namespace in namespaces:
        print(f"- {namespace}")

def edit_resource_pack():
    list_resource_packs()
    while True:
        name = input("Enter the name of the resource pack to edit: ")
        try:
            selected_pack = get_resource_pack(name)
            break
        except FileNotFoundError:
            print(f"Resource pack '{name}' not found. Please try again.")
            
    if selected_pack:
        # Placeholder for editing logic
        print(f"Editing resource pack: {selected_pack.name}")
        while True:
            list_namespaces(selected_pack)
            try:
                namespace = input("Enter the name of the namespace to use or create (or type 'exit' to leave): ")
                if namespace.lower() == 'exit':
                    print("Exiting edit mode.")
                    return None
                namespace = get_namespace(namespace, selected_pack)
                break
            except ValueError as e:
                print(e)

        add_new_model(namespace, selected_pack)

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
    3: ("Export a resource pack", lambda: export_pack(get_resource_pack(input("Enter the name of the resource pack to export: ")))),
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
