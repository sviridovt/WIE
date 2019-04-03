import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from lab7p2 import signFile, verifySignature
from lab7encDec import decFile

certFname = "user1_cert.pem"
fnameDataEnc = "dataEnc.txt"
sigFname = "dataEnc.sig"
fnameDataDec = "dataDec.dat"
fnameKeyEnc = "keyEnc.dat"
sigFname2 = "keyEnc.sig"

backend = default_backend()

verifySignature(fnameDataEnc, sigFname, certFname)

#decrypt secret key
password = 'olleh'

with open("kr2.pem", "rb") as file:
    private_key = serialization.load_pem_private_key(
        data=file.read(), 
        password=password.encode(),
        backend=backend)
file.close()

with open(fnameKeyEnc, "rb") as file:
    data = file.read()
file.close()
    
secret_key = private_key.decrypt(data, padding.PKCS1v15())

ivval = "ivpass"

decFile(fnameDataEnc, fnameDataDec, ivval)
