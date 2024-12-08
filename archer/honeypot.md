
# Clone of Archer Router as a Honeypot with Telegram bot Notifications

## **Objective**
The primary goal of this project was to design and implement a functional clone of an Archer router interface to act as a honeypot. The system was required to achieve the following:

1. Provide Telegram notifications when:
   - A user accessed the fake router interface.
   - A user attempted to log in and entered a password.
   - Port scanning activity was detected targeting the honeypot.

2. Include detection mechanisms for port scanning to monitor activities.
3. Ensure seamless integration between the honeypot and Telegram notifications via bot to alert administrator in real-time.

---

## **Project Implementation**


### **Honeypot Interface Design**
A replica of the Archer router's web interface was meticulously created to lure potential attackers. The fake interface mimicked the original's look and feel, including:

<table>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/3d8f3376-c7d3-4fdd-a2fd-6b0751aded39" alt="Original" width="800">
      <div style="text-align: center; font-style: italic;">Original</div>
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/0b5ccda9-7f85-49e6-a8e2-d3de72ed69f4" alt="Honeypot" width="800">
      <div style="text-align: center; font-style: italic;">Honeypot</div>
    </td>
  </tr>
</table>

---

### **Notifications and Event Tracking**
A Telegram bot was implemented to provide real-time notifications. The following events triggered alerts:

1. **Website Access**:
   - Upon visiting the fake router's website, a notification containing the visitor's IP address, timestamp, and User-Agent was sent.
     
   ![image](https://github.com/user-attachments/assets/aeb47ad2-f0fb-41fb-8d1e-896d662919e4)


2. **Password Entry**:
   - When a user attempted to log in by entering credentials, the details (password) were captured and sent via Telegram.
   - Notification included metadata like IP, timestamp, User-Agent and password.

     ![image](https://github.com/user-attachments/assets/1d7c011d-ed18-412c-8fb2-a848d26cb081)

     

3. **Port Scanning Detection**:
   - Custom scripts monitored incoming network traffic for patterns indicative of port scanning.
   - Detected scanning activities were logged and sent to Telegram with:
     - Source IP address
     - Target ports

       ![image](https://github.com/user-attachments/assets/48a36763-0181-45b8-bedd-483f68958ae5)
---
