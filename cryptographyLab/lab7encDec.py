import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

backend = default_backend()

def encFile(fnameData, fnameDataEnc, passwd, ivval, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16, #length in bytes
        salt=salt,
        iterations=100000, #min is 100,000
        backend=backend
        )
    key = kdf.derive(bytes(passwd, "utf8"))

    idf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=100000,
        backend=backend
        )
    iv = idf.derive(bytes(ivval, "utf8"))       #use same key&ivval as task72?
    
    cipher = Cipher(
        algorithm=algorithms.AES(key), 
        mode=modes.CBC(iv),
        backend=backend
        )
    
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    path = os.path.abspath(fnameData)
    path2 = os.path.abspath(fnameDataEnc)

    blocksize=16
    mydata = bytearray(blocksize)
    
    #open the files
    file = open(fnameData, "rb")
    file2 = open(fnameDataEnc, "wb")
    
    #initialize vars for loop
    totalsize = 16
    data = padder.update(salt)
    file2.write(bytearray(data))
    
    while True:
        #read block from source file
        num = file.readinto(mydata)
        totalsize += num

        if num == blocksize:
            data = padder.update(bytes(mydata))
            ciphertext = encryptor.update(data)
            file2.write(bytearray(ciphertext))
        else:
            mydata2 = mydata[0:num]
            data = padder.update(bytes(mydata2)) + padder.finalize()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            file2.write(bytearray(ciphertext))
            break
        
        num += 1
    
    print('encrypting read ', totalsize, ' bytes')
    file.close()
    file2.close()
    return key

def decFile(fnameDataEnc, fnameDataDec, ivval):
    blocksize=16
    mydata = bytearray(blocksize)
    
    file = open(fnameDataEnc, "rb")
    file2 = open(fnameDataDec, "wb")
    
    totalsize = 16

    salt = bytearray(blocksize)
    file.readinto(salt)

    idf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=100000,
        backend=backend
        )
    iv = idf.derive(bytes(ivval, "utf8"))
    
    cipher = Cipher(
        algorithm=algorithms.AES(key), 
        mode=modes.CBC(iv),
        backend=backend
        )
        
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    #pdata = unpadder.update(bytes(salt))
    
    path = os.path.abspath(fnameDataEnc)
    path2 = os.path.abspath(fnameDataDec)
    
    filesize = os.path.getsize(path)

    while True:
        num = file.readinto(mydata)
        totalsize += num

        if totalsize < filesize: #num == blocksize:
            plaintext = decryptor.update(bytes(mydata))
            data = unpadder.update(plaintext)
            file2.write(data)
        else:
            plaintext = decryptor.update(bytes(mydata)) + decryptor.finalize()
            data = unpadder.update(plaintext) + unpadder.finalize()
            
            file2.write(data)
            break
        
    file.close()
    file2.close()