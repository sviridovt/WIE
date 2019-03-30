# allows to import RSA lib from different dir
import sys
import json

# inserts path to access all the libs
sys.path.insert(0, '../libs')

# keychain stores all the RSA keys
from KeyChain import KeyChain

# import decrypt fucntion to verify key
from RSAKeys import decrypt

caPubKeyFile = 'caPriKey.pem'
printDebug = True

# this function has all the logic to verify a certificate
def verify(cert):
  # convert cert to json format
  cert = json.loads(cert)

  # init keychain
  # the externalPubKey will be the caServer pubKey
  keyChain = KeyChain()
  with open(caPubKeyFile) as fd:
    keyChain.externalPubKey = fd.read()
    fd.close()

  # unhash the signiture
  signedHash = cert['signedHash']
  print('here===================')
  print(signedHash)
# TODO make the code below work!!!
#  unHashed = decrypt(signedHash, keyChain.externalPubKey)
  print(unHashed)

  return True
