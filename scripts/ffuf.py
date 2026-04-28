import os
import subprocess
import re
import argparse

parser = argparse.ArgumentParser(description="FFUF URL Scanner")
parser.add_argument("-i", "--input", help="Input file containing payloads (one per line)")
parser.add_argument("-o", "--output", default="ffuf_scan.txt", help="Output file name (default: ffuf_scan.txt)")
parser.add_argument("-u", "--url", default="http://example.com/FUZZ", help="Target URL with FUZZ keyword (default: http://example.com/FUZZ)")
parser.add_argument("-w", "--wordlist", default="~/Pillon_tool/tools/seclists/Discovery/Web-Content/common.txt", help="Custom wordlist file for ffuf")
args = parser.parse_args()
url = "http://"+args.url+"/FUZZ"

def run_ffuf():
    command = f"ffuf -u {args.url} -w {args.wordlist} -o {args.output} -of csv"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"FFUF scan completed for payload: {args.url}")
    except subprocess.CalledProcessError as e:
        print(f"Error running ffuf: {e.stderr.decode()}")

if __name__ == "__main__":
    run_ffuf()