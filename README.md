# **checkIPLeaks — VPN/IP Leak Monitor with Automatic Wi-Fi Kill Switch**

## 📌 Overview

**checkIPLeaks** is a lightweight Windows-based security tool that continuously monitors your public IP address to detect potential VPN or proxy leaks. If your real (non-VPN) IP is detected too many times in a row, the program automatically disables your Wi-Fi interface to prevent unintended exposure of your identity or location.

### The tool is designed for:
- Privacy-conscious users  
- VPN users who want leak protection  
- Security testing and verification  
- Anyone who wants an automated “kill switch” based on IP monitoring  

---

## ✅ Core Functionality

### 🔍 Continuous IP Monitoring
The script periodically checks your current public IP using reliable external services:

- https://api.ipify.org  
- https://ifconfig.me  
- https://ipinfo.io  

If any service fails, it automatically tries the next one.

---

### ⚠️ Leak Detection Logic
A **leak** is detected when your current public IP matches your original (non-VPN) IP.

The program:
- Tracks consecutive IP matches  
- Resets the counter if your VPN IP returns  
- Triggers an action only after a user-defined number of leaks  

---

### ⚡ Automatic Wi-Fi Kill Switch

If the number of detected leaks reaches your chosen threshold, the script automatically disables your Wi-Fi adapter using:

```powershell
netsh interface set interface name="Wi-Fi" admin=disabled


