from flask import Blueprint, request, jsonify
from pki import certificate, verify

bp = Blueprint("pki", __name__, url_prefix="/api/v1")

@bp.route("/issue", methods=["POST"])
def issue():
    data = request.get_json()
    cn = data.get("common_name")
    if not cn:
        return jsonify({"error": "common_name required"}), 400
    result = certificate.issue_certificate(
        cn, data.get("org", "TestOrg"), data.get("country", "IN")
    )
    return jsonify(result), 201

@bp.route("/renew", methods=["POST"])
def renew():
    data = request.get_json()
    cn = data.get("common_name")
    if not cn:
        return jsonify({"error": "common_name required"}), 400
    return jsonify(certificate.renew_certificate(cn)), 200

@bp.route("/revoke", methods=["POST"])
def revoke():
    data = request.get_json()
    cn = data.get("common_name")
    if not cn:
        return jsonify({"error": "common_name required"}), 400
    return jsonify(certificate.revoke_certificate(cn)), 200

@bp.route("/status/<common_name>", methods=["GET"])
def status(common_name):
    return jsonify(certificate.get_cert_status(common_name)), 200

@bp.route("/verify", methods=["POST"])
def verify_cert():
    if "cert" not in request.files:
        return jsonify({"error": "cert file required"}), 400
    cert_pem = request.files["cert"].read()
    valid = verify.verify_cert_signature(cert_pem)
    return jsonify({"valid": valid}), 200

@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200