import os
from core import ensure_required_directories, create_resource_pack, choose_resource_pack, add_new_model, choose_namespace

ensure_required_directories()

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

def get_options(options):
    for key, value in options.items():
        print(f"{key}. {value[0]}")

def choose_option(options):
    while True:
        try:
            choice: int = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice in options.keys():
            options[choice][1]()
            get_options(options)  # Show options again after executing the chosen function
        else:
            print("Invalid choice. Please select a valid option.")

options = {
    1: ["Create a new resource pack", create_resource_pack],
    2: ["Edit an existing resource pack", edit_resource_pack],
}

if __name__ == "__main__":
    print("Welcome to ToolRP! This is a utility to creating and editing resource packs for Minecraft!")
    print("Please select an option:")
    get_options(options)
    choose_option(options)