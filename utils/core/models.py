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


def add_new_model(namespace: str, resource_pack: pathlib.Path, model_file: pathlib.Path, item: str, overwrite: bool = False):
    exist = False  # Flag to track if the model already exists
    mcmeta_path = pathlib.Path(resource_pack / "pack.mcmeta")
    with open(mcmeta_path, "r") as f:
        mcmeta_data = json.load(f)
    version = mcmeta_data["pack"]["pack_format"]

    models_dir = resource_pack / "assets" / namespace / "models" / "item"
    minecraft_dir = resource_pack / "assets" / "minecraft"
    models_dir.mkdir(parents=True, exist_ok=True)

    if not model_file.is_file():
        raise FileNotFoundError(f"Model file {model_file} does not exist.")

    target_model_path = models_dir / model_file.name
    if target_model_path.is_file():
        if not overwrite:
            raise FileExistsError(f"Model file {target_model_path} already exists. Set overwrite=True to replace it.")

    textures = get_textures(namespace, model_file)

    for texture in textures:
        texture_path = pathlib.Path(resource_pack / "assets" / texture)
        texture_path.parent.mkdir(parents=True, exist_ok=True)
        source_texture_path = model_file.parent / texture.split("/")[-1]
        if not source_texture_path.exists():
            raise FileNotFoundError(f"Texture file {source_texture_path} does not exist for model {model_file}.")

    for texture in textures:
        texture_path = pathlib.Path(resource_pack / "assets" / texture)
        texture_path.parent.mkdir(parents=True, exist_ok=True)
        source_texture_path = model_file.parent / texture.split("/")[-1]
        source_texture_path.copy(texture_path)

    minecraft_items_dir = minecraft_dir / "item"
    minecraft_items_dir.mkdir(parents=True, exist_ok=True)
    choose_item_file = minecraft_items_dir / f"{item}.json"

    if choose_item_file.is_file():
        with open(choose_item_file, "r") as f:
            choose_item_data = json.load(f)
    else:
        choose_item_data = make_item_template(version, item)

    for entry in choose_item_data["model"]["entries"]:
        if entry["model"]["model"] == f"{namespace}:item/{model_file.stem}":
            exist = True

    if not exist:
        threshold = len(choose_item_data["model"]["entries"]) + 1
        choose_item_data["model"]["entries"].append(
            make_entry(f"{namespace}:item/{model_file.stem}", threshold)
        )
        choose_item_file.write_text(json.dumps(choose_item_data, indent=4))

    model_file.copy_into(models_dir)

    return target_model_path
