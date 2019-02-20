from Crypto.PublicKey import RSA
from Crypto import Random
from settings import PRIVATE_KEY, PUBLIC_KEY


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