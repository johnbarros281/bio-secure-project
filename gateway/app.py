# gateway/app.py
from flask import Flask, request, jsonify
import requests
import logging
import base64
import os

app = Flask(__name__)

# CONFIGURATION
PATIENT_IP = os.getenv("PATIENT_IP", "192.168.1.51")
SENSOR_URL = f"http://{PATIENT_IP}:5000/vitals"
SECRET_KEY = "AdminSecure123"  # The Password

# SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/monitor', methods=['GET'])
def monitor_patient():
    visitor_ip = request.remote_addr
    provided_key = request.args.get('key')
    
    # Fetch Data from Pi Zero
    try:
        response = requests.get(SENSOR_URL, timeout=3)
        if response.status_code == 200:
            patient_data = response.json()
        else:
            return jsonify({"error": "Sensor Error"}), 500
    except Exception as e:
        return jsonify({"error": "Connection Failed"}), 500

    # The Bouncer Logic
    if provided_key == SECRET_KEY:
        # AUTHORIZED
        logging.info(f"✅ AUTHORIZED ACCESS: IP {visitor_ip} viewed clear patient data.")
        return jsonify({
            "status": "ACCESS GRANTED",
            "data": patient_data
        })
    else:
        # UNAUTHORIZED (Encryption Simulation)
        raw_string = str(patient_data)
        encrypted_blob = base64.b64encode(raw_string.encode()).decode()
        
        logging.warning(f"🚫 UNAUTHORIZED ACCESS: IP {visitor_ip} saw encrypted blob.")
        return jsonify({
            "status": "ACCESS DENIED",
            "message": "Invalid key. Data is encrypted.",
            "encrypted_payload": encrypted_blob
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
