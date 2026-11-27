import pathlib
import json
from shutil import make_archive
from ..config import (
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


def get_namespace(namespace: str, resource_pack: pathlib.Path):
    assets_dir = resource_pack / "assets"
    namespaces = [d.name for d in assets_dir.iterdir() if d.is_dir()]

    if not namespace:
        raise ValueError("Namespace cannot be empty. Please provide a valid namespace.")

    if namespace not in namespaces:
        new_namespace_dir = assets_dir / namespace
        new_namespace_dir.mkdir()

    return namespace


def create_resource_pack(name: str, version: str | None = None):
    pack_dir = RESOURCE_PACKS_DIR / name
    if pack_dir.exists():
        raise FileExistsError(f"Resource pack '{name}' already exists. Please choose a different name.")
    else:

        if not version:
            version = list(versions.keys())[
                0
            ]  # Default to the latest version if no input is provided

        if version not in versions:
            raise ValueError(f"Version '{version}' is not supported. Supported versions: {list(versions.keys())}")

        pack_dir.mkdir()
        assets_dir = pack_dir / "assets"
        assets_dir.mkdir()

        minecraft_dir = assets_dir / "minecraft"
        minecraft_dir.mkdir()

        with open(pack_dir / "pack.mcmeta", "w") as f:
            f.write(
                json.dumps(
                    make_mcmeta_template(versions[version]["pack_format"]), indent=4
                )
            )

        return pack_dir


def get_resource_pack(name: str):
    pack = RESOURCE_PACKS_DIR / name
    if not pack.exists():
        raise FileNotFoundError(f"Resource pack '{name}' does not exist.")
    return pack


def export_pack(resource_pack: pathlib.Path):
    if not resource_pack:
        print("No resource pack selected for export.")
        return
    output_dir = EXPORTED_PACKS_DIR
    output_dir.mkdir(exist_ok=True, parents=True)
    make_archive(str(output_dir / resource_pack.stem), "zip", root_dir=resource_pack)
    print(f"Exported resource pack '{resource_pack.stem}' as a zip file.")
