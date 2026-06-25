# 🔐 PKI Certificate Lifecycle Automation Tool

> Automate the complete lifecycle of x509 digital certificates — issuance, renewal, and revocation — using a Python-based Mock CA with a REST API interface.

🔗 **Live API:** https://pki-certificate-lifecycle-automation-tool.onrender.com/api/v1/health

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=for-the-badge&logo=flask&logoColor=white)
![OpenSSL](https://img.shields.io/badge/OpenSSL-3.4.6-721412?style=for-the-badge&logo=openssl&logoColor=white)
![Java](https://img.shields.io/badge/Java-11%2B-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔑 Key Generation | RSA-2048 key pair generation |
| 📜 Certificate Issuance | CSR creation + signing via Mock CA |
| 🔄 Auto Renewal | Revoke old cert and issue fresh one |
| ❌ Revocation | CRL-based certificate revocation |
| ✅ Verification | Digital signature verification |
| ☕ Java Interface | Cross-language API client in Java |

---

## 🏗 Architecture

```
Client Request
      │
      ▼
┌─────────────┐
│  Flask API  │  ← REST endpoints (issue/renew/revoke/verify)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   PKI Core  │  ← keygen, csr, certificate modules
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Mock CA   │  ← signs CSRs, manages CRL (revoked.json)
└─────────────┘
       │
       ▼
┌─────────────┐
│   Storage   │  ← certs/, keys/, crl/
└─────────────┘
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/issue` | Issue a new x509 certificate |
| `POST` | `/api/v1/renew` | Renew an existing certificate |
| `POST` | `/api/v1/revoke` | Revoke a certificate |
| `GET` | `/api/v1/status/<cn>` | Check certificate status |
| `POST` | `/api/v1/verify` | Verify certificate signature |
| `GET` | `/api/v1/health` | Health check |

---

## 🚀 Local Setup

```bash
cd PKI-Certificate-Lifecycle-Automation-Tool
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
mkdir storage storage\certs storage\keys storage\crl
python app.py
```

Server runs at `http://localhost:5000`

---

## 📬 Sample API Usage

**Issue a Certificate**
```json
POST /api/v1/issue
{
  "common_name": "example.com",
  "org": "TestOrg",
  "country": "IN"
}
```

**Response**
```json
{
  "common_name": "example.com",
  "serial": "355968043828154334...",
  "not_before": "2026-06-25T11:20:24+00:00",
  "not_after": "2027-06-25T11:20:24+00:00",
  "status": "VALID"
}
```

---

## ☕ Java Client

```java
PKIClient pki = new PKIClient();
System.out.println(pki.issueCert("example.com"));
System.out.println(pki.getCertStatus("example.com"));
System.out.println(pki.revokeCert("example.com"));
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

```
tests/test_pki.py::test_health   PASSED
tests/test_pki.py::test_issue    PASSED
tests/test_pki.py::test_status   PASSED
tests/test_pki.py::test_revoke   PASSED
tests/test_pki.py::test_renew    PASSED
```

---

## 📁 Project Structure

```
├── api/
│   └── routes.py         # Flask REST endpoints
├── pki/
│   ├── ca.py             # Mock Certificate Authority
│   ├── certificate.py    # Issue, renew, revoke logic
│   ├── csr.py            # CSR creation
│   ├── keygen.py         # RSA-2048 key generation
│   └── verify.py         # Signature verification
├── java_client/
│   └── PKIClient.java    # Java API interface
├── tests/
│   └── test_pki.py
├── app.py
├── config.py
└── requirements.txt
```

---

<p align="center">
Built with 🔐 by <a href="https://linkedin.com/in/harshitasoni22">Harshita Soni</a> • B.Tech CSE (Cybersecurity) • JECRC University
</p>