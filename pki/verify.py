from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import config

def verify_cert_signature(cert_pem: bytes) -> bool:
    """Verify cert was signed by our Mock CA."""
    with open(config.CA_CERT_PATH, "rb") as f:
        ca_cert = x509.load_pem_x509_certificate(f.read())
    cert = x509.load_pem_x509_certificate(cert_pem)
    try:
        ca_cert.public_key().verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False