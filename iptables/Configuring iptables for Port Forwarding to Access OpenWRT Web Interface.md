# Step 1: Check Your Local Machine’s IP Address

1. Open a terminal.
2. Run:
   ```bash
   ip addr show
   ```
3. Look for the `inet` address under the active interface (e.g., `wlan1` or `eth0`).

# Step 2: Identify Your Router’s IP Address

1. SSH into the router:
   ```bash
   ssh root@<router_IP>
   ```
2. Run:
   ```bash
   ip addr show
   ```
   - Find the `inet` address for the `br-lan` or relevant interface.

# Step 3: Enable IP Forwarding on the Local Machine

1. Enable temporarily:
   ```bash
   echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
   ```
2. Make it persistent:
   ```bash
   sudo nano /etc/sysctl.conf
   ```
   - Add:
     ```
     net.ipv4.ip_forward=1
     ```
   - Save and apply:
     ```bash
     sudo sysctl -p
     ```

# Step 4: Configure iptables for Port Forwarding

1. Choose a local port (e.g., `8080`).
2. Add rules:
   ```bash
   sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 172.16.1.102:80
   sudo iptables -t nat -A POSTROUTING -j MASQUERADE
   ```
3. Verify:
   ```bash
   sudo iptables -t nat -L -n -v
   ```

# Step 5: Test the Configuration

1. Open a browser on another device and navigate to:
   ```
   http://<local_machine_IP>:8080
   ```
   - Example:
     ```
     http://192.168.0.115:8080
     ```
2. The OpenWRT web interface should appear. I attempted to access the specified address of the laptop from my phone, and it worked perfectly. The OpenWRT web interface successfully opened. A screenshot of the result is attached.

<img src="https://github.com/user-attachments/assets/217910a5-006c-4535-aaa0-d1e32f1ad6fe" alt="Screenshot" width="25%">

