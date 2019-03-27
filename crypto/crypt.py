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
from encDec import encFile, decFile
from task7signAndVer import signAndVerify

from hashSignVerify import hashFile, createSig, verifySignature
from rsaGenerate import keyGenerate


#read file and encrypt
#write to file2
#create keys
#read file2 and hash and sign
#send data
#write data to file
#verify sig
#unhash and decrypt
#write new data to file?


#read file and encrypt
fnameData = "file.txt"
fnameDataEnc = "fileEnc.txt"
#hFile = "hashFile.txt"
sigFname = "fileEnc.sig"
fnameKeyEnc = "keyEnc.dat"
sigFname2 = "keyEnc.sig"

fnameDataDec = "dataDec.dat"        #does it need to be .dat?

backend = default_backend()
passwd = os.urandom(16) #"password"
ivval = os.urandom(16)  #"ivpass"
salt = os.urandom(16)


key = encFile(mydata, blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

#create keys
krFname, kuFname = keyGenerate(password)   #change file names of keys & pass into function?

#read file2 and hash and sign
sig = createSig(fnameDataEnc, sigFname, krFname, password)


#send sig

#send data
#write data to file

#verify sig
verifySig(fname, sig, kuFname)

#unhash and decrypt
dataDec = decFile(mydata, blocksize, ivval, key, blocksize)     #how to keep key secret?




backend = default_backend()
salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=16,
    salt=salt,
    iterations=100000,
    backend=backend
)

idf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=16,
    salt=salt,
    iterations=100000,
    backend=backend
)

passwd = "pass"
ivval = "pass"

key = kdf.derive(bytes(passwd, "utf8"))
iv = idf.derive(bytes(ivval, "utf8"))

cipher = Cipher(
    algorithm = algorithms.AES(key),
    mode = modes.CBC(iv),
    backend = backend
)

#encrypt
fname = "outfile.txt"
fname2 = "outinfile2.txt"

path = os.path.abspath(fname)
path2 = os.path.abspath(fname2)

password = "hello"

blocksize = 16
totalsize = 0
mydata = bytearray(blocksize)

#load and hash data to be signed, from task 1
file = open(fname, 'rb')
#file2 = open(fname2, 'wb')

myhash = hashes.MD5()
hasher = hashes.Hash(myhash, backend)
count = 0
datatotal = ""

#decryptor = cipher.decryptor()
#unpadder = padding.PKCS7(128).unpadder()

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
        hasher.update(data)

        #plaintext = decryptor.update(bytes(mydata))
        #mydata_unpad = unpadder.update(plaintext)
        #file2.write(plaintext)

    else:
        # extract subarray
        mydata2 = mydata[0:num]
        data = bytes(mydata2)
        hasher.update(data)
        digest = hasher.finalize()

        #plaintext = decryptor.update(bytes(mydata)) + decryptor.finalize()
        #mydata_unpad = unpadder.update(plaintext) + unpadder.finalize()
        #3file2.write(plaintext)
        break
    
# close files (note will also flush destination file)
file.close()
#file2.close()

# print totalsize
print('read ', totalsize, ' bytes')


#load private key from task 5
kr_fname = bytes("kr.pem", "utf8")
ku_fname = bytes("ku.pem", "utf8")


signAndVerify(kr_fname, ku_fname, password, backend, digest, myhash)

#fname2 = "outinfile2.txt"
decryptFile(fname, fname2, cipher)
print(3)

"""
-generate AES private/public keys and distribute
-how to keep key/etc private
-using networking, write input data to file
    -encrypt, send, etc
-make work in server side too