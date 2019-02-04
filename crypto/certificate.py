from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

def signedCertificate(kr_fname, ku_fname, password, commonName, certName):
    
    # Load private & public key pair
    backend = default_backend()

    with open(kr_fname, 'rb') as file:
        private_key = serialization.load_pem_private_key(
            data = file.read(),
            password = password.encode(),
            backend = backend
        )
        file.close()
    with open(ku_fname, 'rb') as file:
        public_key = serialization.load_pem_public_key(
            data = file.read(),
            backend = backend
        )
        file.close()
    
    #create subject and issuer of the certificate as the same person    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME,u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,u"Florida"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Coral Gables"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"University of Miami"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"ECE Dept"),
        x509.NameAttribute(NameOID.COMMON_NAME, commonName),])
    
    #create certificate builder object
    builder = x509.CertificateBuilder()
    
    #set subject and issuer that were just created
    builder = builder.subject_name(subject)
    builder = builder.issuer_name(issuer)
    
    #set the date
    builder = builder.not_valid_before(datetime.today() - timedelta(days=1))
    builder = builder.not_valid_after(datetime(2018,12,22))
    
    #set a random serial number
    builder = builder.serial_number(x509.random_serial_number())
    
    #add public key
    builder = builder.public_key(public_key)
    
    #Add basic extensions
    builder = builder.add_extension(x509.BasicConstraints(ca=False,path_length=None), critical=True)
    
    #sign the certificate
    certificate = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend())
    
    #save the certificate
    with open(certName,'wb') as file:
        file.write(certificate.public_bytes(serialization.Encoding.PEM))
        
#signedCertificate('kr.pem', 'ku.pem', 'hello', u"User1", 'user1_cert.pem')
signedCertificate('kr2.pem', 'ku2.pem', 'olleh', u"User2", 'user2_cert.pem')
