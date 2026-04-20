import os
import subprocess

def run_nmap():
    print("=== Nmap Scan ===")
    target = input("Enter target IP/Domain: ")
    if not target.strip():
        print("Target cannot be empty.")
        return

    folder_name = input("Enter specific folder name for the machine (inside 'machines'): ")
    if not folder_name.strip():
        print("Folder name cannot be empty.")
        return

    # Assuming the script is run from the root of Pillon_tool
    target_dir = os.path.join("machines", folder_name)
    
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        print(f"[-] Failed to create directory {target_dir}: {e}")
        return

    # Using -oN for normal nmap output
    output_file = os.path.join(target_dir, "nmap_scan.txt")
    
    # Constructing the nmap command
    cmd = f"nmap -sV -sC -oN \"{output_file}\" {target}"
    print(f"\n[*] Running command: {cmd}")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"\n[+] Scan complete! Output saved to: {output_file}")
    except subprocess.CalledProcessError:
        print("\n[-] Nmap scan failed or was interrupted.")
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")

if __name__ == "__main__":
    run_nmap()
