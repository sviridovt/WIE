import os
import io
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends.openssl import backend

myhash = hashes.MD5()
hasher = hashes.Hash(myhash, backend)
count = 0
datatotal = ""

while count < 4:
    msg = input("Please input a line: ")
    data = bytes(msg, 'utf-8')
    datatotal += msg
    hasher.update(data)
    count += 1

digest = hasher.finalize()

print(digest)
print(datatotal)