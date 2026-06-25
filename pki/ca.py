from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import datetime, os, json
import config

REVOKED_DB = os.path.join(config.STORAGE["crl"], "revoked.json")

def _load_revoked():
    if os.path.exists(REVOKED_DB):
        with open(REVOKED_DB) as f:
            return json.load(f)
    return {}

def _save_revoked(db):
    with open(REVOKED_DB, "w") as f:
        json.dump(db, f, indent=2)

def bootstrap_ca():
    os.makedirs(config.STORAGE["certs"], exist_ok=True)
    os.makedirs(config.STORAGE["keys"], exist_ok=True)
    os.makedirs(config.STORAGE["crl"], exist_ok=True)
    os.makedirs(os.path.dirname(config.CA_KEY_PATH), exist_ok=True)
    
    if os.path.exists(config.CA_CERT_PATH):
        return load_ca()
    key = rsa.generate_private_key(65537, 2048, default_backend())
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "Mock Root CA"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PKI Demo"),
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )
    with open(config.CA_KEY_PATH, "wb") as f:
        f.write(key.private_bytes(serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()))
    with open(config.CA_CERT_PATH, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    return key, cert

def load_ca():
    with open(config.CA_KEY_PATH, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), None)
    with open(config.CA_CERT_PATH, "rb") as f:
        cert = x509.load_pem_x509_certificate(f.read())
    return key, cert

def sign_csr(csr, validity_days=365):
    ca_key, ca_cert = load_ca()
    cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=validity_days))
        .sign(ca_key, hashes.SHA256())
    )
    return cert

def revoke_cert(serial_number: int):
    db = _load_revoked()
    db[str(serial_number)] = datetime.datetime.utcnow().isoformat()
    _save_revoked(db)

def is_revoked(serial_number: int) -> bool:
    return str(serial_number) in _load_revoked()