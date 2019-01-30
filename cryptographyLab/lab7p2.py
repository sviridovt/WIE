from task7signAndVer import signAndVerify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from encodings.base64_codec import base64_encode, base64_decode
import base64


def hashFile(fname):
    blocksize = 16
    totalsize = 0
    mydata = bytearray(blocksize)

    #load and hash data to be signed, from task 1
    file = open(fname, 'rb')
    myhash = hashes.MD5()
    hasher = hashes.Hash(myhash, backend)

    while True:
        num = file.readinto(mydata)
        totalsize += num
    
        print(num, mydata)

        if num == blocksize:
            data = bytes(mydata)
            hasher.update(data)

        else:
            mydata2 = mydata[0:num]
            data = bytes(mydata2)
            hasher.update(data)
            digest = hasher.finalize()
            break

    return(myhash, digest)

def createSig(fname, sigFname, kr_fname, password):
    #fname2 = "infile.txt"
    myhash, digest = hashFile(fname)

    with open(kr_fname, 'rb') as file:
        private_key = serialization.load_pem_private_key(
            data = file.read(),
            password = password.encode(),
            backend = backend
        )
    file.close()

    pad = padding.PKCS1v15()

    sig = private_key.sign(
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )
    #save signature to file
    #fname = "user1.sig"  #"signature.sig"
    file = open(sigFname, 'wb')
    file.write(bytes("-----BEGIN SIGNATURE-----\n", 'utf8'))
    file.write(base64_encode(sig)[0])
    #file.write(s)
    file.write(bytes("-----END SIGNATURE-----", 'utf8'))


def signFile(fname, sigFname, kr_name, password):
    """
    pem_kr = "kr.pem"   #'../kr.pem'
    password_u1 = "hello"
    sigFname = "user1.sig"  #'../user1.sig'
    fname = "infile.txt"    #'../out2.txt'
    """

    createSig(fname, sigFname, kr_name, password)

def verifySignature(fname, sigFname, certFname):
   # sigFname = "user1.sig"

    #fname = "infile.txt"

    myhash, digest = hashFile(fname)

    #with open("user1_cert.pem","rb") as file:
    with open(certFname,"rb") as file:
         certificate = x509.load_pem_x509_certificate(
             data=file.read(),
             backend=backend)
    file.close()

    with open(sigFname, "rb") as file:
        temp = file.read()
        sig = temp[26:-24]
        sig = base64.b64decode(sig)
    file.close()

    public_key = certificate.public_key()

    pad = padding.PKCS1v15()

    public_key.verify(
        signature = sig,
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )


def verifyCertificate():
    with open("user1_cert.pem", "rb") as file:
        certificate = x509.load_pem_x509_certificate(
            data=file.read(),
            backend=backend)
    public_key = certificate.public_key()
    sig = certificate.signature
    data = certificate.tbs_certificate_bytes
    
    myhash = hashes.SHA256()
    hasher = hashes.Hash(myhash, backend)
    
    hasher.update(bytes(data))
    digest = hasher.finalize()
    
    #verify the certificate
    pad = padding.PKCS1v15()

    public_key.verify(
        signature = sig,
        data = digest,
        padding = pad,
        algorithm = utils.Prehashed(myhash)
    )
#verifyCertificate()
signFile("infile.txt", "dataEnc.sig", "kr.pem", "hello")