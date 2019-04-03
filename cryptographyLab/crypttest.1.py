import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from encodings.base64_codec import base64_encode

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

#kpass = b'hello'
#key = kdf.derive(kpass)
#print(key.hex())

idf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=16,
    salt=salt,
    iterations=100000,
    backend=backend
)

#ivpass = b'bye'
#iv = ivdf.derive(ivpass)
#print(iv.hex())

passwd = b'password'
ivval = b'hello'

key = kdf.derive(passwd)
iv = idf.derive(ivval)

print(key.hex())
print(iv.hex())

cipher = Cipher(
    algorithm = algorithms.AES(key),
    mode = modes.ECB(),
    backend = backend
)

encryptor = cipher.encryptor()

mydata = b'1234567812345678'
print(mydata)
padder = padding.PKCS7(128).padder()
#unpadder = padding.PKCS7(128).unpadder()
mydata_pad = padder.update(mydata) + padder.finalize()
print(mydata_pad.hex())
ciphertext = encryptor.update(mydata_pad) + encryptor.finalize()
print(ciphertext.hex())

decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext)+decryptor.finalize()
#plain3 = unpadder.update(plain2)+unpadder.finalize()
print("plaintext hex: ", plaintext.hex())
print("plaintext: ", plaintext)
print("b64 encoded key: ", base64_encode(key))
print("b64 encoded iv: ", base64_encode(iv))
print("b64 encoded ciphertext: ", base64_encode(ciphertext))

