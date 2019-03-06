from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from settings import PRIVATE_KEY, PUBLIC_KEY
import base64


def genKeyPair(pubKeyName = PUBLIC_KEY, privKeyName = PRIVATE_KEY):
    key = RSA.generate(8192, Random.new().read)

    priv = key.exportKey()
    pub = key.publickey().exportKey()

    print(priv)
    fd = open(privKeyName, 'wb')
    fd.write(priv)
    fd.close()

    print(pub)
    fd = open(pubKeyName, 'wb')
    fd.write(pub)
    fd.close()


def encrypt(text, key):
    key = RSA.importKey(key)
    encrypted = key.encrypt(text, 3422)
    print(encrypted)
    return encrypted


def encrypt_private(text, key):
    key = RSA.importKey(key)
    encryptor = PKCS1_OAEP.new(key)
    encrypted = encryptor.encrypt(text)
    print(encrypted)
    return encrypted


def decrypt_public(encrypted, key):
    key = RSA.importKey(key)
    encryptor = PKCS1_OAEP.new(key)
    decrypted = encryptor.decrypt(encrypted)
    return decrypted


def decrypt(text, key):
    key = RSA.importKey(key)
    decrypted = key.decrypt(text)
    print(decrypted)
    return decrypted