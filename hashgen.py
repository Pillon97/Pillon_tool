import hashlib

password = str(input("Enter input: "))
print(hashlib.sha256(password.encode()).hexdigest())