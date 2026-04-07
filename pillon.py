import subprocess
import json
import matrix
import os
import login
import hashlib
import getpass
import datetime

def log_install(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("install.log", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_config():
    if not os.path.exists("config.json") or os.stat("config.json").st_size == 0:
        # Return a default structure if the file doesn't exist or is empty
        return {"installed": False, "username": "", "password": "", "tools": [], "dependencies": []}
    with open("config.json") as f:
        return json.load(f)

config = load_config()

def start():
    matrix.matrix(50)
    clear()
    print("\033[31m", end="")
    print("""#########################################################################
#                                                                       #
#     ██████╗ ██╗██╗     ██╗      ██████╗ ███╗   ██╗ █████╗ ███████╗    #
#     ██╔══██╗██║██║     ██║     ██╔═══██╗████╗  ██║██╔══██╗╚════██║    #
#     ██████╔╝██║██║     ██║     ██║   ██║██╔██╗ ██║╚██████║    ██╔╝    #
#     ██╔═══╝ ██║██║     ██║     ██║   ██║██║╚██╗██║ ╚═══██║   ██╔╝     #
#     ██║     ██║███████╗███████╗╚██████╔╝██║ ╚████║ █████╔╝   ██║      #
#     ╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚════╝    ╚═╝      #
#                                                                       #
#########################################################################""")


    print("Wellcome Pillon!")

    login.login()

    clear()
    
    input("Press Enter to continue...")
    #print("Check updates...")
    #subprocess.run("apt update", shell=True, check=True)
    #subprocess.run("apt upgrade -y", shell=True, check=True)
    #print("Done!")


def menu():
    clear()
    print("Menu")
    print("1. Install tools")
    print("2. Check for updates")
    print("3. tools")
    print("4. Exit")

    x = int(input("Choose an option: "))
    if x == 1:
        for tool in config["tools"]:
            print(f"\n[+] Installing {tool['name']}")
            log_install(f"User initiated install for tool: {tool['name']}")
            run_install(tool["install"])
        for dep in config["dependencies"]:
            print(f"\n[+] Installing dependency: {dep['name']}")
            log_install(f"User initiated install for dependency: {dep['name']}")
            run_install(dep["install"])
    elif x == 2:
        print("Check updates...")
        subprocess.run("apt update", shell=True, check=True)
        subprocess.run("apt upgrade -y", shell=True, check=True)
        print("Done!")
    elif x == 3:
        print("Tools:")
    elif x == 4:
        print("Exiting...")
        exit()
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



def run_install(cmd):

    try:
        print(f"[>] {cmd}")
        log_install(f"Executing command: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
        log_install(f"Successfully executed: {cmd}")
    except subprocess.CalledProcessError:
        print(f"[-] Failed: {cmd}")
        log_install(f"FAILED to execute: {cmd}")

def install_deps(cmd):
    try:
        print(f"[>] Installing dependencies for: {cmd}")
        log_install(f"Installing dependencies for: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
        log_install(f"Successfully installed dependencies for: {cmd}")
    except subprocess.CalledProcessError:
        print(f"[-] Failed to install dependencies for: {cmd}")
        log_install(f"FAILED to install dependencies for: {cmd}")

def register_user():
    username = input("Enter new username: ")
    password = getpass.getpass("Enter new password: ")
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    log_install(f"User registered: {username}")
    data = load_config()
    data["username"] = username_hash
    data["password"] = password_hash
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

def installed():
    data = load_config()
    data["installed"] = True
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)
    log_install("Installation status updated to: True")

def folders():
    try:
        target_folders = ["tools", "machines", "exploits", "payloads", "scripts", "templates"]
        for folder in target_folders:
            os.makedirs(folder, exist_ok=True)
            log_install(f"Directory created/verified: {folder}")
    except Exception as e:
        print(f"[-] Failed to create folders: {e}")
        log_install(f"CRITICAL: Failed to create folders: {e}")
        exit()



if __name__ == "__main__":
    #print(config["installed"])
    if config["installed"] == False:
        log_install("Starting first-time setup/installation process.")
        register_user()
        for tool in config["tools"]:
            print(f"\n[+] Installing {tool['name']}")
            log_install(f"Installing tool: {tool['name']}")
            run_install(tool["install"])
        for dep in config["dependencies"]:
            print(f"\n[+] Installing dependency: {dep['name']}")
            log_install(f"Installing dependency: {dep['name']}")
            run_install(dep["install"])
        folders()
        installed()
        log_install("First-time setup completed successfully.")
        start()
        menu()
    else:
        print("Already installed!")
        input("Press Enter to continue...")
        start()
        menu()