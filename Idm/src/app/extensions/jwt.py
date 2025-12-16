import jwt
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
import os
load_dotenv()
crt_data = os.getenv("PathCrt") 
key_data = os.getenv("PathKey")
with open(f"{crt_data}", "rb") as certif_file:
   cert_data = certif_file.read()
   certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
public_key1 = certificate.public_key()
with open(f"{key_data}", "rb") as key_file:

    private_key1 = serialization.load_pem_private_key(

       key_file.read(),

        password=None,

  )
private_key = rsa.generate_private_key(
       public_exponent=65537,
       key_size=2048,
       backend=default_backend()
)
public_key = private_key.public_key()
private_pem = private_key.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.PKCS8,
       encryption_algorithm=serialization.NoEncryption()
   )
public_pem = public_key.public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
   )
jwt_api = jwt