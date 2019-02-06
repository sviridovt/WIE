import os
import io
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from encodings.base64_codec import base64_encode
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


private_key = rsa.generate_private_key(
    public_exponent = 65537,
    key_size = 2048,
    backend = backend
)

public_key = private_key.public_key()

password = "hello"  #read hash of superuser password from linux password file 
pem_kr = private_key.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.PKCS8,
    encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
)

pem_ku = public_key.public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo
)

kr_fname = bytes("kr.pem", "utf8")
ku_fname = bytes("ku.pem", "utf8")
path1 = os.path.abspath(kr_fname)
path2 = os.path.abspath(ku_fname)
file1 = open(kr_fname, 'wb')
file2 = open(ku_fname, 'wb')
file1.write(pem_kr)
file2.write(pem_ku)
file1.close()
file2.close()

with open(kr_fname, 'rb') as file:
    private_key = serialization.load_pem_private_key(
        data = file.read(),
        password = password.encode(),
        backend = backend
    )
    file.close()
with open(ku_fname, 'rb') as file:
    public_key = serialization.load_pem_public_key(
        data = file.read(),
        backend = backend
    )
    file.close()
print(private_key)  #0x1048ebe80
print(public_key)   #0x10442f4e0
