# vitals.py
from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

DEVICE_ID = "INSULIN-PUMP-001"

@app.route('/vitals', methods=['GET'])
def get_vitals():
    # Simulate realistic vitals
    heart_rate = random.randint(60, 90)
    spo2 = random.randint(94, 100) 
    
    data = {
        "device_id": DEVICE_ID,
        "timestamp": time.time(),
        "heart_rate": heart_rate,
        "oxygen_saturation": spo2,
        "status": "normal" if spo2 > 95 else "alert"
    }
    
    # VULNERABILITY: Returning this as standard HTTP (unencrypted)
    return jsonify(data)

if __name__ == '__main__':
    # host='0.0.0.0' exposes it to the network
    app.run(host='0.0.0.0', port=5000)
