from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import time
import random

# Initialize Flask app
app = Flask(__name__)

# Firebase initialization using service account
cred = credentials.Certificate("serviceAccountKey.json")
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
    # Port 5000 for Render deployment
    app.run(host="0.0.0.0", port=5000)
