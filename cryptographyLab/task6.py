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
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from encodings.base64_codec import base64_encode


#encrypt
fname = "infile.txt"
fname2 = "outfile2.txt"

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
    
# close files (note will also flush destination file)
file.close()
#file2.close()

# print totalsize
print('read ', totalsize, ' bytes')


#load private key from task 5
kr_fname = bytes("kr.pem", "utf8")
#ku_fname = bytes("ku.pem", "utf8")

with open(kr_fname, 'rb') as file:
    private_key = serialization.load_pem_private_key(
        data = file.read(),
        password = password.encode(),
        backend = backend
    )
    file.close()
    
"""with open(ku_fname, 'rb') as file:
    public_key = serialization.load_pem_public_key(
        data = file.read(),
        backend = backend
    )
    file.close()"""


#pad hashed data
pad = padding.PSS(
    mgf = padding.MGF1(hashes.SHA256()),
    salt_length = padding.PSS.MAX_LENGTH
)

#pad = padding.PKCS1v15()

#sign data with private key
sig = private_key.sign(
    data = digest,
    padding = pad,
    algorithm = utils.Prehashed(myhash)
)
#print(sig)
#s = base64.b64decode(sig)#.decode('utf8')
#print(s)

#save signature to file
fname = "signature.sig"
file = open(fname, 'wb')
file.write(bytes("-----BEGIN SIGNATURE-----\n", 'utf8'))
file.write(base64_encode(sig)[0])
#file.write(s)
file.write(bytes("-----END SIGNATURE-----", 'utf8'))
"""
#save signature to file
fname = "user1.sig"  #"signature.sig"
file = open(fname, 'wb')
file.write(bytes("-----BEGIN SIGNATURE-----\n", 'utf8'))
file.write(base64_encode(sig)[0])
#file.write(s)
file.write(bytes("-----END SIGNATURE-----", 'utf8'))
"""