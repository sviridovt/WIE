# allows to import RSA lib from different dir
import sys
import datetime, json
from libs import RSAKeys
from Crypto.PublicKey import RSA
from datetime import datetime
from Crypto.Hash import MD5, SHA256
import binascii
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
  hash = cert['signedHash']
  SSID = cert['SSID']
  print(SSID)
  #need to convert to date
  expiration = cert['expiration']
  # datetime_expiration = datetime.strptime(expiration, '%Y-%m-%d')
  # print(datetime_expiration)
  pubKey = cert['pubKey']
  ca = cert['ca']
  caKey = open('caPubKey.pem', 'r')
  # caKey = RSA.importKey(caKey.read())
  verCert = {
    'SSID': SSID,
    'expiration': cert['expiration'],
    'pubKey': pubKey,
    'ca': ca,
  }
  jsData = json.dumps(verCert)
  verHash = SHA256.new(jsData.encode('utf-8')).digest()
  # print(hash)

  hash = RSAKeys.decrypt(hash, caKey.read())
  print(hash)
  print(verHash)
  # convert cert to json format
  # cert = json.loads(cert)

  # init keychain
  # the externalPubKey will be the caServer pubKey
  # keyChain = KeyChain()
  # with open(caPubKeyFile) as fd:
  #   keyChain.externalPubKey = fd.read()
  #   fd.close()

  # unhash the signiture
  # signedHash = cert['signedHash']
  # print('here===================')
  # print(signedHash)
# TODO make the code below work!!!
#  unHashed = decrypt(signedHash, keyChain.externalPubKey)
#   print(unHashed)

  return True

fl = open('cert.txt', 'r')
cert = json.load(fl)
print(cert)
print(verify(cert))
