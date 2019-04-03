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
file2 = open(fname2, 'wb')

myhash = hashes.MD5()
hasher = hashes.Hash(myhash, backend)
count = 0
datatotal = ""

decryptor = cipher.decryptor()
unpadder = padding.PKCS7(128).unpadder()

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

        plaintext = decryptor.update(bytes(mydata))
        mydata_unpad = unpadder.update(plaintext)
        file2.write(plaintext)

    else:
        # extract subarray
        mydata2 = mydata[0:num]
        data = bytes(mydata2)
        hasher.update(data)
        digest = hasher.finalize()

        plaintext = decryptor.update(bytes(mydata)) + decryptor.finalize()
        mydata_unpad = unpadder.update(plaintext) + unpadder.finalize()
        file2.write(plaintext)
        break
    
# close files (note will also flush destination file)
file.close()
file2.close()

# print totalsize
print('read ', totalsize, ' bytes')


#load private key from task 5
kr_fname = bytes("kr.pem", "utf8")
ku_fname = bytes("ku.pem", "utf8")

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
fname2 = "outinfile2.txt"

#path = os.path.abspath(fname)
path2 = os.path.abspath(fname2)

decryptor = cipher.decryptor()
#padder = padding.PKCS7(128).padder()
#unpadder = padding.PKCS7(128).unpadder()

#print('copying ', path, 'to ', path2)
blocksize = 16
totalsize = 0
#mydata = bytearray(blocksize)
#file = open(fname, 'rb')
file2 = open(fname2, 'wb')


plaintext = decryptor.update(bytes(data)) + decryptor.finalize()
print("plaintext in hex ", plaintext.hex())
#mydata_unpad = unpadder.update(plaintext) + unpadder.finalize()
#print("mydata unpad in hex ", mydata_unpad.hex())
        

# write subarray to destination and break loop
file2.write(plaintext)
#break
    
# close files (note will also flush destination file)
#file.close()
file2.close()"""