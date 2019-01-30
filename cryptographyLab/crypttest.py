import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# regenerate iv
# keep salt -> save to file
# file -> encrypt -> out
# also need decryption
# given salt and pw

backend = default_backend()

salt = os.urandom(16)

print(salt.hex())

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=16,
    salt=salt,
    iterations=100000,
    backend=backend
)

kpass = b'hello'
key = kdf.derive(kpass)
print(key.hex())

ivdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=16,
    salt=salt,
    iterations=100000,
    backend=backend
)

ivpass = b'bye'
iv = ivdf.derive(ivpass)
print(iv.hex())

cipher = Cipher(
    algorithm = algorithms.AES(key),
    mode = modes.CBC(iv),
    backend = backend
)

encryptor = cipher.encryptor()

plain = b'1234567812345678'

padder = padding.PKCS7(128).padder()
unpadder = padding.PKCS7(128).unpadder()

pdata = padder.update(plain) + padder.finalize()

ciphertext = encryptor.update(pdata) + encryptor.finalize()

decryptor = cipher.decryptor()
plain2 = decryptor.update(ciphertext) + decryptor.finalize()
plain3 = unpadder.update(plain2) + unpadder.finalize()
print(plain3.hex())
print(plain2.hex())
print(pdata.hex())
print(plain.hex())
