from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Util import number
import datetime, json, settings, RSAKeys


def newCert(SSID, pubKey, len = datetime.timedelta(days=90)):
    cert = {
        'SSID': SSID,
        'expiration': datetime.date.today() + len,
        'pubKey': pubKey,
    }
    cert['expiration'] = cert['expiration'].isoformat()
    jsData = json.dumps(cert)
    hash = MD5.new(jsData.encode('utf-8')).digest()

    fl = open(settings.PRIVATE_KEY, 'rb')
    key = fl.read()
    fl.close()
    hash = RSAKeys.encrypt(hash, key)

    print(hash)
    cert.update({
        'signedHash': hash,
    })
    print(json.dumps(cert))

newCert("TEST", "etstdksaljfdkl;asfjkldas;jgk")