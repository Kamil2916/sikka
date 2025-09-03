from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import os
import time
import random

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Firebase initialization using environment variables
cred_dict = {
    "type": os.environ["FIREBASE_TYPE"],
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "client_id": os.environ["FIREBASE_CLIENT_ID"],
    "auth_uri": os.environ["FIREBASE_AUTH_URI"],
    "token_uri": os.environ["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["FIREBASE_AUTH_PROVIDER_CERT_URL"],
    "client_x509_cert_url": os.environ["FIREBASE_CLIENT_CERT_URL"]
}

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sikkamahal-default-rtdb.asia-southeast1.firebasedatabase.app'
})

@app.route("/referral", methods=["POST"])
def save_referral():
    data = request.json

    # Get referral code from request body
    referral_code = data.get("code")
    if not referral_code:
        return jsonify({"error": "Referral code missing"}), 400

    # Get user IP
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Generate unique ID
    temp_id = f"web_{int(time.time()*1000)}_{random.randint(1000,9999)}"

    # Save to Firebase Realtime Database
    db.reference(f"pendingReferrals/{temp_id}").set({
        "code": referral_code,
        "ip": user_ip,
        "timestamp": int(time.time()*1000)
    })

    return jsonify({"success": True, "id": temp_id, "ip": user_ip})

if __name__ == "__main__":
    # Use Render's dynamic port or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
