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
#from task7dec import decryptFile



def signAndVerify(kr_fname, ku_fname, password, backend, digest, myhash):
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


    #pad hashed data
    pad = padding.PSS(
        mgf = padding.MGF1(hashes.SHA256()),
        salt_length = padding.PSS.MAX_LENGTH
    )
   


    sig = private_key.sign(
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )


    public_key.verify(
        signature = sig,
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )

"""

def createSig(fname):
    myhash = hashes.MD5()
    hasher = hashes.Hash(myhash, backend)

    while True:
    # read block from source file
    num = file.readinto(mydata)

    # adjust totalsize
    totalsize += num
    
    # print data, assuming text data
    print(num, mydata)
    # use following if raw binary data
    #print(num, data.hex())

    # check if full block read
    if num == blocksize:
        data = bytes(mydata)
        #datatotal += msg
        hasher.update(data)
        #count += 1

    else:
        # extract subarray
        mydata2 = mydata[0:num]
        data = bytes(mydata2)
        #datatotal += msg
        hasher.update(data)
        digest = hasher.finalize()
        break

    sig = private_key.sign(
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )
    #save signature to file
    #fname = "signature.sig"
    file = open(fname, 'wb')
    file.write(bytes("-----BEGIN SIGNATURE-----\n", 'utf8'))
    file.write(base64_encode(sig)[0])
    #file.write(s)
    file.write(bytes("-----END SIGNATURE-----", 'utf8'))


"""

"""
def signFile(kr_fname, ku_fname, password, backend, digest, myhash):
    pem_kr = "kr.pem"   #'../kr.pem'
    password_u1 = "hello"
    sig_file = "user1.sig"  #'../user1.sig'
    fname = "infile.txt"    #'../out2.txt'
    """