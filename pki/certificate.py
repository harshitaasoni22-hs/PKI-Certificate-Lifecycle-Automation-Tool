from cryptography.hazmat.primitives import serialization
from cryptography import x509
import os, config
from pki import keygen, csr as csr_module, ca as ca_module

def issue_certificate(common_name: str, org="TestOrg", country="IN"):
    private_key, key_path = keygen.generate_key_pair(common_name)
    csr, _ = csr_module.create_csr(private_key, common_name, org, country)
    cert = ca_module.sign_csr(csr)
    cert_path = os.path.join(
        config.STORAGE["certs"], f"{common_name}.cert.pem"
    )
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    return {
        "common_name": common_name,
        "serial": str(cert.serial_number),
        "not_before": cert.not_valid_before.isoformat(),
        "not_after": cert.not_valid_after.isoformat(),
        "cert_path": cert_path,
        "key_path": key_path,
    }

def renew_certificate(common_name: str):
    """Revoke old cert, issue fresh one with same name."""
    cert_path = os.path.join(
        config.STORAGE["certs"], f"{common_name}.cert.pem"
    )
    if os.path.exists(cert_path):
        with open(cert_path, "rb") as f:
            old_cert = x509.load_pem_x509_certificate(f.read())
        ca_module.revoke_cert(old_cert.serial_number)
    return issue_certificate(common_name)

def revoke_certificate(common_name: str):
    cert_path = os.path.join(
        config.STORAGE["certs"], f"{common_name}.cert.pem"
    )
    if not os.path.exists(cert_path):
        return {"error": "Certificate not found"}
    with open(cert_path, "rb") as f:
        cert = x509.load_pem_x509_certificate(f.read())
    ca_module.revoke_cert(cert.serial_number)
    return {"revoked": True, "serial": str(cert.serial_number)}

def get_cert_status(common_name: str):
    cert_path = os.path.join(
        config.STORAGE["certs"], f"{common_name}.cert.pem"
    )
    if not os.path.exists(cert_path):
        return {"status": "NOT_FOUND"}
    with open(cert_path, "rb") as f:
        cert = x509.load_pem_x509_certificate(f.read())
    revoked = ca_module.is_revoked(cert.serial_number)
    return {
        "common_name": common_name,
        "serial": str(cert.serial_number),
        "not_before": cert.not_valid_before.isoformat(),
        "not_after": cert.not_valid_after.isoformat(),
        "status": "REVOKED" if revoked else "VALID",
    }