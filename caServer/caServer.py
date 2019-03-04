import os, RSAKeys, settings
from db import db
from Crypto.PublicKey import RSA

if not (os.path.exists(settings.PUBLIC_KEY) and os.path.exists(settings.PRIVATE_KEY)):
    try:
        RSAKeys.genKeyPair()
    except PermissionError:
        print("Permission error, cant create certificate files")
        exit(1)

fl = open(settings.PUBLIC_KEY, 'rb')
privKey = RSA.importKey(fl.read())
fl.close()

fl = open(settings.PRIVATE_KEY, 'rb')
pubKey = RSA.importKey(fl.read())
fl.close()

db = db.Database()
db = db.db.data

print(db)