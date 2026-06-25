from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os
import config

def generate_key_pair(name: str):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=config.KEY_SIZE,
        backend=default_backend()
    )
    key_path = os.path.join(config.STORAGE["keys"], f"{name}.key.pem")
    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    return private_key, key_path

def load_private_key(name: str):
    key_path = os.path.join(config.STORAGE["keys"], f"{name}.key.pem")
    with open(key_path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)
    