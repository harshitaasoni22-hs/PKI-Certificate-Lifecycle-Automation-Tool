from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
import os
import config

def create_csr(private_key, common_name: str, org: str = "TestOrg", country: str = "IN"):
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        ]))
        .sign(private_key, hashes.SHA256())
    )
    csr_path = os.path.join(
        config.STORAGE["certs"], f"{common_name}.csr.pem"
    )
    with open(csr_path, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))
    return csr, csr_path