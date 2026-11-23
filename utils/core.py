import pathlib
import json
from shutil import make_archive
from config import make_mcmeta_template, versions, make_item_template, make_entry

PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]
RESOURCE_PACKS_DIR = PROJECT_DIR / "resource_packs"
EXPORTED_PACKS_DIR = PROJECT_DIR / "exported_packs"

def ensure_required_directories():
    dir_path = RESOURCE_PACKS_DIR
    if not dir_path.exists():
        dir_path.mkdir()
        print(f"Created required directory: {dir_path}")

def create_resource_pack():
    name = input("Enter the name of the new resource pack: ")
    pack_dir = RESOURCE_PACKS_DIR / name
    if pack_dir.exists():
        print(f"A resource pack with the name '{name}' already exists. Try a different name.")
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
            version = input("Enter the version of minecraft, you would like to create(default latest): ")
            if not version:
                version = list(versions.keys())[0] # Default to the latest version if no input is provided
                print("Choosing the latest version by default.")
                break

            if version in versions:
                break
            
            print(f"Version '{version}' is not supported. Please choose from the following versions: {', '.join(versions.keys())}")
        
        with open(pack_dir / "pack.mcmeta", "w") as f:
            f.write(json.dumps(make_mcmeta_template(versions[version]["pack_format"]), indent=4))

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

def choose_namespace(resource_pack: pathlib.Path):
    assets_dir = resource_pack / "assets"
    namespaces = [d.name for d in assets_dir.iterdir() if d.is_dir()]
    print(f"Available namespaces in {resource_pack.name}:")
    
    for namespace in namespaces:
        print(f"- {namespace}")
    
    print("Create a new namespace by entering a name, or select an existing one by typing its name.")
    chosen_namespace = input("Enter the name of the namespace: ")
    
    if not chosen_namespace:
        return None
    
    if chosen_namespace not in namespaces:
        new_namespace_dir = assets_dir / chosen_namespace
        new_namespace_dir.mkdir()
        print(f"Created new namespace: {chosen_namespace}")

    return chosen_namespace

def get_textures(namespace: str, model_file: pathlib.Path):
    textures_dir = namespace + "/textures"
    with open(model_file, "r") as f:
        model_data = json.load(f)
    textures: dict = model_data.get("textures", {})
    return ["/".join([textures_dir, texture.split(":")[1]+".png"]) for texture in textures.values()]

def add_new_model(namespace: str, resource_pack: pathlib.Path):
    mcmeta_path = pathlib.Path(resource_pack / "pack.mcmeta")
    with open(mcmeta_path, "r") as f:
        mcmeta_data = json.load(f)
    version = mcmeta_data["pack"]["pack_format"]

    models_dir = resource_pack / "assets" / namespace / "models" / "item"
    minecraft_dir = resource_pack / "assets" / "minecraft"
    models_dir.mkdir(parents=True, exist_ok=True)

    model_path = input("Enter a path to the model file you want to add (e.g., 'models/my_item.json'): ")
    model_file = pathlib.Path(model_path)
    model_file.copy_into(models_dir)

    choose_item = input("Enter the name of the item you want add the model to (e.g., 'paper'): ")
    minecraft_items_dir = minecraft_dir / "item"
    minecraft_items_dir.mkdir(parents=True, exist_ok=True)
    choose_item_file = minecraft_items_dir / f"{choose_item}.json"

    if choose_item_file.exists():
        with open(choose_item_file, "r") as f:
            choose_item_data = json.load(f)
    else:
        choose_item_data = make_item_template(version, choose_item)
    threshold = len(choose_item_data["model"]["entries"]) + 1
    choose_item_data["model"]["entries"].append(make_entry(f"{namespace}:item/{model_file.stem}", threshold))
    choose_item_file.write_text(json.dumps(choose_item_data, indent=4))

    for texture in get_textures(namespace, model_file):
        texture_path = pathlib.Path(resource_pack / "assets" / texture)
        texture_path.parent.mkdir(parents=True, exist_ok=True)
        source_texture_path = model_file.parent / texture.split("/")[-1]
        print(f"Copying texture from '{source_texture_path}' to '{texture_path}'")
        if source_texture_path.exists():
            source_texture_path.copy(texture_path)
        else:
            print(f"Warning: Texture file '{source_texture_path}' not found. Skipping.")
    
    print(f"Added model '{model_file.name}' to item '{choose_item}' in resource pack '{resource_pack.name}'.")

def add_new_sound(namespace: str, resource_pack: pathlib.Path):
    print("Functionality to add new sounds is not yet implemented.")

def export_pack(resource_pack: pathlib):
    if not resource_pack:
        print("No resource pack selected for export.")
        return
    output_dir = EXPORTED_PACKS_DIR
    output_dir.mkdir(exist_ok=True, parents=True)
    make_archive(str(output_dir / resource_pack.stem), 'zip', root_dir=resource_pack)
    print(f"Exported resource pack '{resource_pack.stem}' as a zip file.")
    
if __name__ == "__main__":
    print(get_textures("test", pathlib.Path("models/charm_coin.json")))  # Example usage of get_textures function
    export_pack(RESOURCE_PACKS_DIR / "test")