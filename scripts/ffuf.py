import os
import subprocess
import re

def is_ip(target):
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", target) is not None
def is_domain(target):
    return re.match(r"^([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$", target) is not None

def run_ffuf():
    print("=== ffuf Scan ===")
    
    target = input("Enter target IP/Domain: ").strip()
    while not target:
        print("Target cannot be empty.")
        target = input("Enter target IP/Domain: ").strip()
        
    folder_name = input("Enter specific folder name for the machine (inside 'machines'): ").strip()
    while not folder_name:
        print("Folder name cannot be empty.")
        folder_name = input("Enter specific folder name for the machine (inside 'machines'): ").strip()

    target_dir = os.path.join("machines", folder_name)
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        print(f"[-] Failed to create directory {target_dir}: {e}")
        return

    common_wordlist = "tools/SecLists/Discovery/Web-Content/common.txt"
    subdomain_wordlist = "tools/SecLists/Discovery/DNS/subdomains-top1million-110000.txt"
    
    output_file = os.path.join(target_dir, "ffuf_scan.txt")
    
    if is_ip(target):
        print("[*] Target is an IP address. Running directory discovery...")
        ip = f"http://{target}"
        cmd = f"ffuf -u {ip}/FUZZ -w {common_wordlist} -o \"{output_file}\" -of md"
    elif is_domain(target):
        print("[*] Target is a Domain. Running subdomain/vhost discovery...")
        domain = target.replace("http://", "").replace("https://", "")
        url = f"http://{domain}"
    else:
        print("[*] Target is not an IP address or Domain.")
        return
    print(f"\n[*] Running command: {cmd}")
    subdomain_scan = input("[Y/N] Would you like to run a subdomain scan?")
    if subdomain_scan.lower() == "y":
        cmd = f"ffuf -u {url}/FUZZ -w {subdomain_wordlist} -o \"{output_file}\" -of md"
        print(f"\n[*] Running command: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"\n[+] Scan complete! Output saved to: {output_file}")
    except subprocess.CalledProcessError:
        print("\n[-] ffuf scan failed or was interrupted.")
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")

if __name__ == "__main__":
    run_ffuf()