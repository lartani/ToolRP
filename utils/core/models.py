import pathlib
import json
from ..config import (
    make_mcmeta_template,
    versions,
    make_item_template,
    make_entry,
    RESOURCE_PACKS_DIR,
)


def get_textures(namespace: str, model_file: pathlib.Path):
    textures_dir = namespace + "/textures"
    with open(model_file, "r") as f:
        model_data = json.load(f)
    textures: dict = model_data.get("textures", {})
    return [
        "/".join(
            [
                textures_dir,
                (texture.split(":", 1)[1] if ":" in texture else texture) + ".png",
            ]
        )
        for texture in textures.values()
    ]


def add_new_model(namespace: str, resource_pack: pathlib.Path):
    mcmeta_path = pathlib.Path(resource_pack / "pack.mcmeta")
    with open(mcmeta_path, "r") as f:
        mcmeta_data = json.load(f)
    version = mcmeta_data["pack"]["pack_format"]

    models_dir = resource_pack / "assets" / namespace / "models" / "item"
    minecraft_dir = resource_pack / "assets" / "minecraft"
    models_dir.mkdir(parents=True, exist_ok=True)

    while True:
        model_path = input(
            "Enter a path to the model file you want to add (e.g., 'models/my_item.json'): "
        )      
        model_file = pathlib.Path(model_path)
        if not model_file.exists():
            print(f"Error: The file '{model_file}' does not exist. Please try again.")
            continue

        try:
            model_file.copy_into(models_dir)
        except OSError as e:
            print(f"Details: {e}")
            continue
        break

    
    choose_item = input(
        "Enter the name of the item you want add the model to (e.g., 'paper'): "
    )
    minecraft_items_dir = minecraft_dir / "item"
    minecraft_items_dir.mkdir(parents=True, exist_ok=True)
    choose_item_file = minecraft_items_dir / f"{choose_item}.json"

    if choose_item_file.exists():
        with open(choose_item_file, "r") as f:
            choose_item_data = json.load(f)
    else:
        choose_item_data = make_item_template(version, choose_item)
    threshold = len(choose_item_data["model"]["entries"]) + 1
    choose_item_data["model"]["entries"].append(
        make_entry(f"{namespace}:item/{model_file.stem}", threshold)
    )
    choose_item_file.write_text(json.dumps(choose_item_data, indent=4))

    for texture in get_textures(namespace, model_file):
        texture_path = pathlib.Path(resource_pack / "assets" / texture)
        texture_path.parent.mkdir(parents=True, exist_ok=True)
        source_texture_path = model_file.parent / texture.split("/")[-1]
        if source_texture_path.exists():
            print(f"Copying texture from '{source_texture_path}' to '{texture_path}'")
            source_texture_path.copy(texture_path)
        else:
            print(f"Warning: Texture file '{source_texture_path}' not found.")
            skip = input(f"Do you want to skip adding the texture '{texture}'? (y/n):")
            if skip.lower() == "y":
                print(f"Skipping texture '{texture}'.")
            else:
                return print(f"Please ensure the texture file '{source_texture_path}' exists.")

    return print(
        f"Added model '{model_file.name}' to item '{choose_item}' in resource pack '{resource_pack.name}'."
    )


if __name__ == "__main__":
    namespace = "my_namespace"
    resource_pack = RESOURCE_PACKS_DIR / "test"
    add_new_model(namespace, resource_pack)
