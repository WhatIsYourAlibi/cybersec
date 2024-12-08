import socket
from datetime import datetime

def port_scanner(target_ip, start_port, end_port):
    """Scan a range of ports on the target IP."""
    print(f"Starting scan on {target_ip} from port {start_port} to {end_port}...")
    start_time = datetime.now()

    for port in range(start_port, end_port + 1):
        try:
            # Create a socket connection to the target port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Timeout for the connection attempt
                result = s.connect_ex((target_ip, port))  # Connect to the target IP and port

                if result == 0:  # If the connection is successful
                    print(f"Port {port}: Open")
                else:
                    print(f"Port {port}: Closed")
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

    end_time = datetime.now()
    print(f"Scan completed in {end_time - start_time}.")

if __name__ == "__main__":
    # Target server IP and port range to scan
    target_ip = "127.0.0.1"  # Replace with your server's IP
    start_port = 10        # Starting port of the range
    end_port = 100          # Ending port of the range

    # Run the scanner
    port_scanner(target_ip, start_port, end_port)
