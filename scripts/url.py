import argparse
from urllib.parse import quote_plus

parser = argparse.ArgumentParser(description="URL encode payloads from input file, generate range, or interactively and save to output file.")
parser.add_argument("-i", "--input", help="Input file containing payloads (one per line)")
parser.add_argument("-o", "--output", default="wordlist.txt", help="Output file name (default: wordlist.txt)")
parser.add_argument("-g", "--generate", nargs=2, type=int, metavar=("START", "END"), help="Generate numbers from START to END (inclusive)")

args = parser.parse_args()

output_file = args.output

if args.input:
    try:
        with open(args.input, "r") as f:
            payloads = f.readlines()
        with open(output_file, "a") as f:
            for payload in payloads:
                payload = payload.strip()
                if payload:
                    encoded = quote_plus(payload)
                    f.write(encoded + "\n")
        print(f"Encoded payloads from {args.input} written to {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
elif args.generate:
    start, end = args.generate
    with open(output_file, "a") as f:
        for num in range(start, end + 1):
            encoded = quote_plus(str(num))
            f.write(encoded + "\n")
    print(f"Generated numbers from {start} to {end} written to {output_file}")
else:
    payload = input("Enter the payload: ")
    encoded = quote_plus(payload)
    with open(output_file, "a") as f:
        f.write(encoded + "\n")
    print(f"Encoded payload written to {output_file}")