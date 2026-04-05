import subprocess
import json
import matrix
import os
import login

with open("config.json") as f:
    config = json.load(f)

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
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

    #print("installed = True")

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
    print(f"[+] Successfully installed dependencies for: {cmd}")
    with open("config.json", "r") as f:
        data = json.load(f)
    data["installed"] = True  # ← csak ezt módosítod
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)



if __name__ == "__main__":
    #print(config["installed"])
    if config["installed"] == False:
        start()
        for tool in config["tools"]:
            print(f"\n[+] Installing {tool['name']}")
            run_install(tool["install"])
        for dep in config["dependencies"]:
            print(f"\n[+] Installing dependency: {dep['name']}")
            run_install(dep["install"])
    else:
        print("Already installed!")
        input("Press Enter to continue...")
        start()
        menu()