import os
import io
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from encodings.base64_codec import base64_encode

def hashFile(fname):
    blocksize = 16
    totalsize = 0
    mydata = bytearray(blocksize)

    #load and hash data to be signed, from task 1
    file = open(fname, 'rb')
    myhash = hashes.MD5()
    hasher = hashes.Hash(myhash, backend)

    while True:
        num = file.readinto(mydata)
        totalsize += num
    
        print(num, mydata)

        if num == blocksize:
            data = bytes(mydata)
            hasher.update(data)

        else:
            mydata2 = mydata[0:num]
            data = bytes(mydata2)
            hasher.update(data)
            digest = hasher.finalize()
            break

    return(myhash, digest)

def createSig(fname, sigFname, kr_fname, password):
    #fname2 = "infile.txt"
    myhash, digest = hashFile(fname)

    with open(kr_fname, 'rb') as file:
        private_key = serialization.load_pem_private_key(
            data = file.read(),
            password = password.encode(),
            backend = backend
        )
    file.close()

    pad = padding.PKCS1v15()

    sig = private_key.sign(
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )


def verifySignature(fname, sigFname, certFname):
   # sigFname = "user1.sig"

    #fname = "infile.txt"

    myhash, digest = hashFile(fname)

    #with open("user1_cert.pem","rb") as file:
    with open(certFname,"rb") as file:
         certificate = x509.load_pem_x509_certificate(
             data=file.read(),
             backend=backend)
    file.close()

    with open(sigFname, "rb") as file:
        temp = file.read()
        sig = temp[26:-24]
        sig = base64.b64decode(sig)
    file.close()

    public_key = certificate.public_key()

    pad = padding.PKCS1v15()

    public_key.verify(
        signature = sig,
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )