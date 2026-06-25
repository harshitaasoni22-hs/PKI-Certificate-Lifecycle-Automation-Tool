import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STORAGE = {
    "certs": os.path.join(BASE_DIR, "storage", "certs"),
    "keys":  os.path.join(BASE_DIR, "storage", "keys"),
    "crl":   os.path.join(BASE_DIR, "storage", "crl"),
}

KEY_SIZE = 2048
CERT_VALIDITY_DAYS = 365
CA_CERT_PATH = os.path.join(BASE_DIR, "storage", "ca_cert.pem")
CA_KEY_PATH  = os.path.join(BASE_DIR, "storage", "ca_key.pem")
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"