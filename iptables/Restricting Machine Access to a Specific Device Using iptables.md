
# Step 1: Reset Existing iptables Rules

1. Open the terminal.
2. Run the following commands to reset all current iptables rules:
   ```bash
   sudo iptables -F
   sudo iptables -X
   sudo iptables -t nat -F
   sudo iptables -t nat -X
   sudo iptables -t mangle -F
   sudo iptables -t mangle -X
   ```
   These commands flush all rules and delete any user-defined chains in the `filter`, `nat`, and `mangle` tables.
# Step 2: Set Default Policy to Drop Incoming Traffic

1. Set the default policy for the `INPUT` chain to `DROP`:
   ```bash
   sudo iptables -P INPUT DROP
   ```
   This blocks all incoming traffic by default.

# Step 3: Allow Essential Traffic for System Functionality

1. Allow established and related connections to ensure the system can respond to existing connections:
   ```bash
   sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   ```

2. Allow local loopback traffic (`localhost`):
   ```bash
   sudo iptables -A INPUT -i lo -j ACCEPT
   ```

# Step 4: Allow Access Only for the Specific device

1. Add a rule to allow incoming traffic from the iPad's IP address (`192.168.0.101`):
   ```bash
   sudo iptables -A INPUT -s 192.168.0.101 -j ACCEPT
   ```
   This ensures that only the specified IP can access the machine.

# Step 5: Verify iptables Rules

1. Check the current iptables rules to ensure they are configured correctly:
   ```bash
   sudo iptables -L -n -v
   ```
   The output should show:
   - An `ACCEPT` rule for `192.168.0.101`.
   - An `ACCEPT` rule for `ESTABLISHED,RELATED` traffic.
   - An `ACCEPT` rule for `lo` (localhost).
   - A default policy of `DROP` for all other incoming traffic.

# Step 6: Demonstrating Access with Proofs

1. **Access from iPad (Allowed)**:
   - Attempted to connect to the machine from the iPad (IP: `192.168.0.101`). 
   - The connection was successful, as expected. Below is a photo confirming the access:
<img src="https://github.com/user-attachments/assets/463adf0f-77a4-412e-a0bc-be7304df2646" alt="IMG_0154" width="50%">

2. **Access from Phone (Blocked)**:
   - Attempted to connect to the machine from the phone (IP: `192.168.0.105`).
   - The connection was denied, as expected. Below is a photo confirming the blocked access:
<img src="https://github.com/user-attachments/assets/09aca4f5-1a4d-4424-a5e8-f09da43884b2" alt="Screenshot_20241117-214724" width="25%">


This demonstrates that the `iptables` rules were configured correctly to allow access only for the iPad and deny access for all other devices.
