# PKI Certificate Lifecycle Automation Tool

A Python-based tool to automate PKI certificate lifecycle management — generation, renewal, and revocation of x509 digital certificates using OpenSSL.

🔗 **Live Demo:** https://pki-certificate-lifecycle-automation-tool.onrender.com/api/v1/health

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-REST%20API-lightgrey?style=flat&logo=flask)
![OpenSSL](https://img.shields.io/badge/OpenSSL-3.4.6-red?style=flat)
![Java](https://img.shields.io/badge/Java-11%2B-orange?style=flat&logo=java)

---

## Features

- Generate RSA-2048 key pairs and x509 digital certificates
- Automate CSR creation and certificate signing via Mock CA
- REST API endpoints for certificate issuance, renewal, and revocation
- Digital signature verification
- Certificate Revocation List (CRL) management
- Java-compatible API interface for cross-language integration

---

## Project Structure
---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/issue` | Issue a new certificate |
| POST | `/api/v1/renew` | Renew an existing certificate |
| POST | `/api/v1/revoke` | Revoke a certificate |
| GET | `/api/v1/status/<cn>` | Check certificate status |
| POST | `/api/v1/verify` | Verify certificate signature |
| GET | `/api/v1/health` | Health check |

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/harshitaasoni22-hs/PKI-Certificate-Lifecycle-Automation-Tool.git
cd PKI-Certificate-Lifecycle-Automation-Tool

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create storage directories
mkdir storage storage\certs storage\keys storage\crl

# Run the app
python app.py
```

---

## Sample API Usage

**Issue a Certificate**
```bash
curl -X POST https://pki-certificate-lifecycle-automation-tool.onrender.com/api/v1/issue \
  -H "Content-Type: application/json" \
  -d '{"common_name": "example.com", "org": "TestOrg", "country": "IN"}'
```

**Check Certificate Status**
```bash
curl https://pki-certificate-lifecycle-automation-tool.onrender.com/api/v1/status/example.com
```

---

## Java Client

```java
PKIClient pki = new PKIClient();
pki.issueCert("example.com");
pki.getCertStatus("example.com");
pki.revokeCert("example.com");
```

---

## Tests

```bash
pytest tests/ -v
```

5 tests — issue, renew, revoke, status, health — all passing ✅

---

*Built by [Harshita Soni](https://linkedin.com/in/harshitasoni22) • B.Tech CSE (Cybersecurity) • JECRC University*