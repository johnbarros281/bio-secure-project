# bio-secure-project
A quick and simple Raspberry Pi project simulating a medical device sending out sensitive information and connecting to it securely

# 🛡️ Bio-Secure IoT Lab: Securing Vulnerable Medical Infrastructure

## Project Overview

This project simulates a real-world cybersecurity challenge: securing legacy medical IoT devices that transmit sensitive patient data over unencrypted channels.

Using heterogeneous hardware (Raspberry Pi 3 & Pi Zero W), I built a segmented network architecture where a Secure Gateway acts as a reverse proxy, enforcing authentication, encryption, and audit logging before allowing access to a vulnerable "Medical Sensor."
## 🎯 Objective

To demonstrate Network Defense, API Security, and Containerized Infrastructure by moving from a flat, insecure network to a hardened, segmented architecture.
## 🏗️ Network Architecture

Node A (The Gateway): Raspberry Pi 3 Model B (Running Docker + Flask + Pi-hole). Acts as the "Bouncer."

Node B (The Vulnerable Sensor): Raspberry Pi Zero W. Simulates an insecure insulin pump broadcasting raw JSON data.

The Firewall: UFW rules on Node B strictly block all traffic except requests originating from Node A.

## 🔒 Key Security Features
1. Identity & Access Management (IAM)

    Problem: The medical sensor (Node B) had no authentication; anyone on the WiFi could view patient vitals.

    Solution: Implemented a Token-Based Authentication System on the Gateway.

    Result: Requests without the correct ?key=AdminSecure123 token are rejected.

2. Conditional Data Encryption

    Logic: If an unauthorized user attempts to view the dashboard, the system does not just block them; it simulates Encrypted Obfuscation.

    Code Highlight:
```python
    if provided_key != SECRET_KEY:
        # User sees base64 encoded gibberish instead of medical data
        encrypted_blob = base64.b64encode(raw_data.encode()).decode()
        return jsonify({"error": "Access Denied", "payload": encrypted_blob})
```
3. Network Segmentation & Firewalls

    Defense: configured UFW (Uncomplicated Firewall) on the Pi Zero to create a "Allowlist" policy.

    Rule: ALLOW FROM 192.XXX.X.XX TO ANY PORT 5000

    Effect: Direct access attacks (bypassing the gateway) are dropped instantly.

4. Security Auditing & Logging

    Every access attempt is logged with the timestamp, source IP, and access status (Authorized/Unauthorized). This provides a forensic trail for incident response.

## 📸 Proof of Concept (Screenshots)
1. Unauthorized Access Attempt (The "Hacker" View)

The user tries to access the Gateway without a key. Result: Access Denied & Encrypted Payload. ![Unauthorized View]()

2. Authorized Access (The "Doctor" View)

The user provides the correct key. Result: Cleartext JSON data. ![Authorized View](screenshots/authorized.png)
3. Forensic Logs

Docker logs showing the detection of both authorized and unauthorized attempts. ![Logs](screenshots/logs.png)
🛠️ Technologies Used

    Hardware: Raspberry Pi 3B, Raspberry Pi Zero W

    OS: Raspberry Pi OS Lite (64-bit & 32-bit)

    Containerization: Docker & Docker Compose

    Network Security: UFW (Firewall), Pi-hole (DNS Sinkhole)

    Backend: Python (Flask), REST APIs

    Protocol: HTTP/JSON

## 🚀 How to Run

1. The Sensor (Pi Zero W)

```bash
python3 vitals.py
```

2. The Gateway (Pi 3)
```bash
# Build and run the secure container
docker compose up -d --build
```
