import os
#from file_crypt import encrypt_file2
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
#from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#from cryptography.hazmat.primitives import hashes
#from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from lab7p2 import signFile
from lab7encDec import encFile, decFile

fnameData = "infile.txt"
fnameDataEnc = "dataEnc.txt"
sigFname = "dataEnc.sig"
fnameKeyEnc = "keyEnc.dat"
sigFname2 = "keyEnc.sig"

backend = default_backend()
passwd = "password"
ivval = "ivpass"
salt = os.urandom(16)


key = encFile(fnameData, fnameDataEnc, passwd, ivval, salt)

#encrypt the secret key used with the public key of user 2
with open('user2_cert.pem', 'rb') as file:
    certificate = x509.load_pem_x509_certificate(
        data=file.read(), 
        backend=backend)

public_key = certificate.public_key()

# Encrypting secret key with user 2's public key
with open(fnameKeyEnc, 'wb') as file:
    file.write(public_key.encrypt(key, padding.PKCS1v15()))

password = "hello"

#myhash, digest = hashFile(fnameDataEnc)
signFile(fnameDataEnc, sigFname, "kr.pem", password)

#myhash2, digest2 = create_digest(enc_keyfile)
signFile(fnameKeyEnc, sigFname2, "kr.pem", password)