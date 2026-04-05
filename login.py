import hashlib
import getpass
import json
import os

def login():
    if not os.path.exists("config.json") or os.stat("config.json").st_size == 0:
        print("Configuration file is missing or empty. Please run pillon.py to register.")
        return

    with open("config.json") as f:
        config = json.load(f)
        
    stored_username = config["username"]
    stored_password_hash = config["password"]

    username = input("Username: ")
    password = getpass.getpass("Password: ")
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if username_hash == stored_username and password_hash == stored_password_hash:
        print("Login successful!")
    else:
        print("Invalid username or password!")
        login()

if __name__ == "__main__":
    login()