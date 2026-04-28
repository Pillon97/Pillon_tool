import os
import subprocess
import re
import argparse
import make_machine

parser = argparse.ArgumentParser(description="FFUF URL Scanner")
parser.add_argument("-i", "--input", help="Input file containing payloads (one per line)")
parser.add_argument("-o", "--output", default="ffuf_scan.txt", help="Output file name (default: ffuf_scan.txt)")
parser.add_argument("-u", "--url", default="http://example.com/FUZZ", help="Target URL with FUZZ keyword (default: http://example.com/FUZZ)")
parser.add_argument("-w", "--wordlist", default="~/Pillon_tool/tools/SecLists/Discovery/Web-Content/common.txt", help="Custom wordlist file for ffuf")
args = parser.parse_args()
url = "http://"+args.url+"/FUZZ"

def run_ffuf():
    print("=== FFUF Scan ===")
    print("Select machine directory or make new one!")
    path = "machines"
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    if not dirs:
        print("No machine directories found.")
        return
    else: 
        for i, d in enumerate(dirs):
            print(f"{i+1}. {d}")
        xid = input("Choose a machine directory (Enter to make new one): ")
        if xid.isdigit() and 1 <= int(xid) <= len(dirs):
            selected_dir = dirs[int(xid)-1]
            print(f"Selected machine directory: {selected_dir}")
        elif xid=="":
            make_machine.make_machine()
        else:
            print("Invalid choice or cancelled.")
            return
        

    
    
    command = f"ffuf -u {url} -w {args.wordlist} -o {selected_dir+'/'+args.output} -of csv"
    try:
        result = subprocess.run(command, shell=True, check=True) 
        print(f"FFUF scan completed for payload: {args.url}")
    except subprocess.CalledProcessError as e:
        print(f"Error running ffuf: {e.stderr.decode()}")

if __name__ == "__main__":
    run_ffuf()