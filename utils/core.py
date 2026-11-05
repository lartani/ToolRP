def test():
    print("Works")

options = {
    1: ["Create a new resource pack", test],
    2: ["Edit an existing resource pack", test],
}

def get_options():
    for key, value in options.items():
        print(f"{key}. {value[0]}")

def choose_option():
    while True:
        try:
            choice: int = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice in options.keys():
            options[choice][1]()
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    print("Welcome to ToolRP! This is a utility to creating and editing resource packs for Minecraft!")
    print("Please select an option:")
    get_options()
    choose_option()