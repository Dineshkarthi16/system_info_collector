import platform
import socket
import psutil
import logging
import os
import smtplib
import ssl
import sys
from pathlib import Path
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

# ----------------------------
# Load .env file (works in .exe too)
# ----------------------------
def load_env():
    if getattr(sys, "frozen", False):  # Running from PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path.cwd()
    env_path = base_path / ".env"
    load_dotenv(env_path)

load_env()

# ----------------------------
# Logging Setup
# ----------------------------
logging.basicConfig(
    filename='system_info.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# ----------------------------
# Collect System Info
# ----------------------------
def get_system_info():
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
    }

    # Disk Info
    disk = psutil.disk_usage('/')
    info["Disk Total (GB)"] = round(disk.total / (1024 ** 3), 2)
    info["Disk Used (%)"] = disk.percent

    # Network Info
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    info["Hostname"] = hostname
    info["IP Address"] = ip_address

    return info

# ----------------------------
# Display & Log Info
# ----------------------------
def display_and_log_info():
    info = get_system_info()
    print("\n📋 SYSTEM INFORMATION:\n")
    for key, value in info.items():
        line = f"{key}: {value}"
        print(line)
        logging.info(line)

# ----------------------------
# Send Email Report
# ----------------------------
def send_email_report():
    email_sender = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_receiver = email_sender  # You can change this if needed

    try:
        with open("system_info.log", "r") as f:
            log_content = f.read()
    except FileNotFoundError:
        print("❌ Log file not found. Run display_and_log_info() first.")
        return

    msg = EmailMessage()
    msg.set_content(log_content)
    msg['Subject'] = 'System Info Report'
    msg['From'] = email_sender
    msg['To'] = email_receiver

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ----------------------------
# Main Program
# ----------------------------
if __name__ == "__main__":
    print("🔧 Collecting system information...")
    display_and_log_info()
    send_email_report()
    print("\n✅ Info logged and emailed.")
    input("\nPress Enter to exit...")
