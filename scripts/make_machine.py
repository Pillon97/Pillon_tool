import os

def make_machine():
    folder_name = input("Enter specific folder name for the machine (inside 'machines'): ")
    if not folder_name.strip():
        print("Folder name cannot be empty.")
        return None

    target_dir = os.path.join("machines", folder_name)

    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        print(f"[-] Failed to create directory {target_dir}: {e}")
        return None
    return target_dir

if __name__ == "__main__":
    make_machine()