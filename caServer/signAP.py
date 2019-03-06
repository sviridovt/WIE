from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Util import number
import datetime, json, settings, RSAKeys
import binascii


def newCert(SSID, pubKey, len = datetime.timedelta(days=90)):
    cert = {
        'SSID': SSID,
        'expiration': datetime.date.today() + len,
        'pubKey': pubKey,
        'ca': 'Fortinet',
    }
    cert['expiration'] = cert['expiration'].isoformat()
    jsData = json.dumps(cert)
    hash = MD5.new(jsData.encode('utf-8')).digest()

    fl = open(settings.PRIVATE_KEY, 'rb')
    key = fl.read()
    fl.close()
    hash = RSAKeys.encrypt_private(hash, key)

    print('hash:', hash)
    cert.update({
        #'signedHash': str(binascii.hexlify(hash[0]))[2:-1],
        'signedHash': str(hash),
    })
    print(json.dumps(cert))
    return cert

#RSAKeys.genKeyPair('demoAPPub', 'demoAPPriv')

f = open('demoAPPub', 'r')

cert = newCert("SecureCanesGuest", f.read())
f.close()
#print(bytes.fromhex(cert['signedHash']))
print(cert['signedHash'])

f = open('SecureCanesGuest.cert', 'w')
json.dump(cert, f)

