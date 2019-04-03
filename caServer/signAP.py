import json
from Crypto.Hash import MD5, SHA256
from Crypto.PublicKey import RSA
from Crypto.Util import number
import datetime, json, settings, RSAKeys
import binascii
from db import db
from caSettings import CA_NAME, PUBLIC_KEY, PRIVATE_KEY

db = db.Database()
# db = db.db.data


def newCert(SSID, pubKey, len = datetime.timedelta(days=90)):
    for data in db.db.data['certs']:
        if data['SSID'] == SSID and data['pubKey'] != pubKey:
            print("SKETCH ALERT: Tring to renew a certificate with different public key, verification failed")
            return 0
        if data['SSID'] == SSID and data['pubKey'] == pubKey:
            del data
    cert = {
        'SSID': SSID,
        'expiration': datetime.date.today() + len,
        'pubKey': pubKey,
        'ca': CA_NAME,
    }
    cert['expiration'] = cert['expiration'].isoformat()
    jsData = json.dumps(cert)
    hash = SHA256.new(jsData.encode('utf-8')).digest()
    print('cert', cert)
    fl = open(PRIVATE_KEY, 'rb')
    key = fl.read()
    fl.close()
    print('pre-encryption', hash)
    hash = RSAKeys.encrypt(hash, key)

    print(str(hash))
    cert.update({
        'signedHash': str(binascii.hexlify(hash[0]))[2:-1],
    })
    print(str(binascii.unhexlify(cert['signedHash'])))
    print(json.dumps(cert))
    db.db.data['certs'].append({
            'SSID': SSID,
            'pubKey': pubKey,
        }
    )
    db.save()
    # return the certificate as a string
    return json.dumps(cert)


# RSAKeys.genKeyPair('pubKey.pem', 'privKey.pem')
#
# f = open('pubKey.pem', 'r')
#
# cert = newCert("SecureCanesGuest", f.read())
# f.close()
# cert = json.loads(cert)
# print(bytes.fromhex(cert['signedHash']))
#
# f = open('SecureCanesGuest.cert', 'w')
# json.dump(cert, f)
#
# print('TRYING TO RENEW WITH WRONG PUBLIC KEY: ')
# cert = newCert('SecureCanesGuest', 'SKETCHYPUBKEY')


