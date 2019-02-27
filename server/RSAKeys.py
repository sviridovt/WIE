from Crypto.PublicKey import RSA
from Crypto import Random
from settings import PRIVATE_KEY, PUBLIC_KEY
import base64


def genKeyPair():
    key = RSA.generate(4096, Random.new().read)

    priv = key.exportKey()
    pub = key.publickey().exportKey()

    print(priv)
    fd = open(PRIVATE_KEY, 'wb')
    fd.write(priv)
    fd.close()

    print(pub)
    fd = open(PUBLIC_KEY, 'wb')
    fd.write(pub)
    fd.close()


def encrypt(text, key):
    key = RSA.importKey(key)
    encrypted = key.encrypt(text, 3422)
    print(encrypted)
    return encrypted


def decrypt(encrypted, key, isString = True):
    if isString:
        encrypted_message = base64.b64decode(encrypted)
    else:
        encrypted_message = encrypted
    key = RSA.importKey(key)
    decrypt = key.decrypt(encrypted_message)
    print(decrypt)
    return decrypt
