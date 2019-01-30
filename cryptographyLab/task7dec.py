import os
import io
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
#from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from encodings.base64_codec import base64_encode


def decryptFile(fname, fname2, cipher):
    
#fname2 = "outinfile2.txt"

    path = os.path.abspath(fname)
    path2 = os.path.abspath(fname2)

    filesize = os.path.getsize(path)

    decryptor = cipher.decryptor()
    #padder = padding.PKCS7(128).padder()
    unpadder = padding.PKCS7(128).unpadder()

    #print('copying ', path, 'to ', path2)
    blocksize = 16
    totalsize = 0
    mydata = bytearray(blocksize)
    file = open(fname, 'rb')
    file2 = open(fname2, 'wb')

    while True:
        num = file.readinto(mydata)
    
        totalsize += num

        if totalsize < filesize:    #num == blocksize:
            plaintext = decryptor.update(bytes(mydata))
            data = unpadder.update(plaintext)
            file2.write(data)
            print(num)
            print(data)
        else:
            #mydata = mydata[0:num]
            plaintext = decryptor.update(bytes(mydata))+decryptor.finalize()
            data = unpadder.update(plaintext)+unpadder.finalize()
            file2.write(data)
            print(num)
            print(data)
            break

        file.close()
        file2.close()
