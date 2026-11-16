import pathlib
from config import MCMETA_TEMPLATE, versions, NEW_TEMPLATE, make_entry

def ensure_required_directories():
    dir_path = pathlib.Path("resource_packs")
    if not dir_path.exists():
        dir_path.mkdir()
        print(f"Created required directory: {dir_path}")

def create_resource_pack():
    name = input("Enter the name of the new resource pack: ")
    pack_dir = pathlib.Path("resource_packs") / name
    if pack_dir.exists():
        print(f"A resource pack with the name '{name}' already exists. Try a different name.")
        create_resource_pack()  # Prompt the user again for a new name
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
            f.write(MCMETA_TEMPLATE.replace("<pack_format>", str(versions[version]["pack_format"])))

        print(f"Created new resource pack: {pack_dir}, with version: {version}")

def choose_resource_pack():
    packs_dir = pathlib.Path("resource_packs")
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
    namespace_dir = resource_pack / "assets"
    namespaces = [d.name for d in namespace_dir.iterdir() if d.is_dir()]
    print(f"Available namespaces in {resource_pack.name}:")
    
    for namespace_dir in namespaces:
        print(f"- {namespace_dir}")
    
    print("Create a new namespace by entering a name, or select an existing one by typing its name.")
    namespace = input("Enter the name of the namespace: ")
    
    if not namespace:
        return None
    
    if namespace not in namespaces:
        new_namespace_dir = namespace_dir / namespace
        new_namespace_dir.mkdir()
        print(f"Created new namespace: {namespace}")

    return namespace

def add_new_model(namespace: str, resource_pack: pathlib.Path):
    models_dir = resource_pack / "assets" / namespace / "models" / "items"
    minecraft_dir = resource_pack / "assets" / "minecraft"
    models_dir.mkdir(parents=True, exist_ok=True)

    model_path = input("Enter a path to the model file you want to add (e.g., 'models/my_item.json'): ")
    model_file = pathlib.Path(model_path)
    model_file.copy_into(models_dir)

    choose_item = input("Enter the name of the item you want add the model to (e.g., 'paper'): ")
    choose_item_file = minecraft_dir / "items" / f"{choose_item}.json"

    choose_item_data = NEW_TEMPLATE.copy()
    threshold = len(choose_item_data["model"]["entries"]) + 1
    choose_item_data["model"]["entries"].append(make_entry(f"{namespace}:{model_file.name}", threshold))
    choose_item_file.write_text(str(NEW_TEMPLATE))

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