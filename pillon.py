import subprocess
import json
import matrix
import os
import login
import hashlib
import getpass

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
            run_install(tool["install"])
        for dep in config["dependencies"]:
            print(f"\n[+] Installing dependency: {dep['name']}")
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
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"[-] Failed: {cmd}")
def install_deps(cmd):
    try:
        print(f"[>] Installing dependencies for: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"[-] Failed to install dependencies for: {cmd}")
def register_user():
    username = input("Enter new username: ")
    password = getpass.getpass("Enter new password: ")
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
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
def folders(cmd):
    try:
        os.makedirs("tools", exist_ok=True)
        os.makedirs("dependencies", exist_ok=True)
        os.makedirs("machines", exist_ok=True)
        os.makedirs("exploits", exist_ok=True)
        os.makedirs("payloads", exist_ok=True)
        os.makedirs("scripts", exist_ok=True)
        os.makedirs("templates", exist_ok=True)
    except Exception as e:
        print(f"[-] Failed to create folders: {e}")
        exit()



if __name__ == "__main__":
    #print(config["installed"])
    if config["installed"] == False:
        register_user()
        for tool in config["tools"]:
            print(f"\n[+] Installing {tool['name']}")
            run_install(tool["install"])
        for dep in config["dependencies"]:
            print(f"\n[+] Installing dependency: {dep['name']}")
            run_install(dep["install"])
        folders()
        installed()
        start()
        menu()
    else:
        print("Already installed!")
        input("Press Enter to continue...")
        start()
        menu()