import pathlib
import json
from shutil import make_archive
from config import (
    make_mcmeta_template,
    versions,
    make_item_template,
    make_entry,
    RESOURCE_PACKS_DIR,
    EXPORTED_PACKS_DIR,
)


def ensure_required_directories():
    dir_path = RESOURCE_PACKS_DIR
    if not dir_path.exists():
        dir_path.mkdir()
        print(f"Created required directory: {dir_path}")


def choose_namespace(resource_pack: pathlib.Path):
    assets_dir = resource_pack / "assets"
    namespaces = [d.name for d in assets_dir.iterdir() if d.is_dir()]
    print(f"Available namespaces in {resource_pack.name}:")

    for namespace in namespaces:
        print(f"- {namespace}")

    print(
        "Create a new namespace by entering a name, or select an existing one by typing its name."
    )
    chosen_namespace = input("Enter the name of the namespace: ")

    if not chosen_namespace:
        return None

    if chosen_namespace not in namespaces:
        new_namespace_dir = assets_dir / chosen_namespace
        new_namespace_dir.mkdir()
        print(f"Created new namespace: {chosen_namespace}")

    return chosen_namespace


def create_resource_pack():
    name = input("Enter the name of the new resource pack: ")
    pack_dir = RESOURCE_PACKS_DIR / name
    if pack_dir.exists():
        print(
            f"A resource pack with the name '{name}' already exists. Try a different name."
        )
        return create_resource_pack()  # Prompt the user again for a new name
    else:
        pack_dir.mkdir()
        assets_dir = pack_dir / "assets"
        assets_dir.mkdir()

        minecraft_dir = assets_dir / "minecraft"
        minecraft_dir.mkdir()
        print("Available Minecraft versions:")

        for ver in versions.keys():
            print(f"- {ver}")

        while True:
            version = input(
                "Enter the version of minecraft, you would like to create(default latest): "
            )
            if not version:
                version = list(versions.keys())[
                    0
                ]  # Default to the latest version if no input is provided
                print("Choosing the latest version by default.")
                break

            if version in versions:
                break

            print(
                f"Version '{version}' is not supported. Please choose from the following versions: {', '.join(versions.keys())}"
            )

        with open(pack_dir / "pack.mcmeta", "w") as f:
            f.write(
                json.dumps(
                    make_mcmeta_template(versions[version]["pack_format"]), indent=4
                )
            )

        print(f"Created new resource pack: {pack_dir}, with version: {version}")


def choose_resource_pack():
    packs_dir = RESOURCE_PACKS_DIR
    packs = [path for path in packs_dir.iterdir() if path.is_dir()]

    if not packs:
        print("No resource packs found. Please create a new resource pack first.")
        return None

    print("Available resource packs:")
    for i, pack in enumerate(packs, start=1):
        print(f"{i}. {pack.name}")

    while True:
        try:
            choice = int(input("Enter resource pack number to edit: "))
            if 1 <= choice <= len(packs):
                selected_pack = packs[choice - 1]
                print(f"Selected resource pack: {selected_pack.name}")
                return selected_pack
            print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def export_pack(resource_pack: pathlib.Path):
    if not resource_pack:
        print("No resource pack selected for export.")
        return
    output_dir = EXPORTED_PACKS_DIR
    output_dir.mkdir(exist_ok=True, parents=True)
    make_archive(str(output_dir / resource_pack.stem), "zip", root_dir=resource_pack)
    print(f"Exported resource pack '{resource_pack.stem}' as a zip file.")
