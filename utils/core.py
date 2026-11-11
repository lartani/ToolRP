import pathlib

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
        print(f"Created new resource pack: {pack_dir}")

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

def edit_resource_pack():
    selected_pack = choose_resource_pack()
    if selected_pack:
        # Placeholder for editing logic
        print(f"Editing resource pack: {selected_pack.name}")