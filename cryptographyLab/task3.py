import os
import io
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

#encrypt
fname = input('Which file would you like to encrypt? ')
fname2 = input('Please provide a name for the output file: ')

path = os.path.abspath(fname)
path2 = os.path.abspath(fname2)

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

passwd = bytes(input("Please provide a password for kdf: "), 'utf-8')
ivval = bytes(input("Please provide a password for IV: "), 'utf-8')

key = kdf.derive(passwd)
iv = idf.derive(ivval)

print("key in hex ", key.hex())
print("iv in hex ", iv.hex())

cipher = Cipher(
    algorithm = algorithms.AES(key),
    mode = modes.CBC(iv),
    backend = backend
)

encryptor = cipher.encryptor()
padder = padding.PKCS7(128).padder()
#unpadder = padding.PKCS7(128).unpadder()

print('copying ', path, 'to ', path2)
blocksize = 16
totalsize = 0
mydata = bytearray(blocksize)
file = open(fname, 'rb')
file2 = open(fname2, 'wb')

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
        # write encrypted full block to destination
        mydata_pad = padder.update(bytes(mydata))
        print("mydata pad in hex ", mydata_pad.hex())
        ciphertext = encryptor.update(mydata_pad)
        print("cipher text in hex ", ciphertext.hex())
        file2.write(ciphertext)

    else:
        # extract subarray
        mydata2 = mydata[0:num]

        mydata_pad = padder.update(bytes(mydata2)) + padder.finalize()
        print("mydata pad in hex ", mydata_pad.hex())
        ciphertext = encryptor.update(mydata_pad) + encryptor.finalize()
        print("cipher text in hex ", ciphertext.hex())

        # write subarray to destination and break loop
        file2.write(ciphertext)
        break
    
# close files (note will also flush destination file)
file.close()
file2.close()

# print totalsize
print('read ', totalsize, ' bytes')




#decrypt
fname = input('Which file would you like to decrypt? ')
fname2 = input('Please provide a name for the output file: ')

path = os.path.abspath(fname)
path2 = os.path.abspath(fname2)

#passwd = bytes(input("Please provide a password for kdf: "), 'utf-8')
#ivval = bytes(input("Please provide a password for IV: "), 'utf-8')

#key = kdf.derive(passwd)
#iv = idf.derive(ivval)

#print("key in hex ", key.hex())
#print("iv in hex ", iv.hex())

decryptor = cipher.decryptor()
#padder = padding.PKCS7(128).padder()
unpadder = padding.PKCS7(128).unpadder()

print('copying ', path, 'to ', path2)
blocksize = 16
totalsize = 0
mydata = bytearray(blocksize)
file = open(fname, 'rb')
file2 = open(fname2, 'wb')

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
        # write encrypted full block to destination
        plaintext = decryptor.update(bytes(mydata))
        print("plaintext in hex ", plaintext.hex())
        mydata_unpad = unpadder.update(plaintext)
        print("mydata unpad in hex ", mydata_unpad.hex())

        file2.write(plaintext)
    else:
        # extract subarray
        mydata2 = mydata[0:num]

        plaintext = decryptor.update(bytes(mydata2)) + decryptor.finalize()
        print("plaintext in hex ", plaintext.hex())
        mydata_unpad = unpadder.update(plaintext) + unpadder.finalize()
        print("mydata unpad in hex ", mydata_unpad.hex())
        

        # write subarray to destination and break loop
        file2.write(plaintext)
        break
    
# close files (note will also flush destination file)
file.close()
file2.close()

# print totalsize
print('read ', totalsize, ' bytes')





#decryptor = cipher.decryptor()
#plaintext = decryptor.update(ciphertext)+decryptor.finalize()
#plain3 = unpadder.update(plain2)+unpadder.finalize()
print("plaintext hex: ", plaintext.hex())
print("plaintext: ", plaintext)
print("b64 encoded key: ", base64_encode(key))
print("b64 encoded iv: ", base64_encode(iv))
print("b64 encoded ciphertext: ", base64_encode(ciphertext))

