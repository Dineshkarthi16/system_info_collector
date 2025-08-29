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
from tkinter import Tk, Text, Button, Label, END

# ----------------------------
# Load .env (works in .exe too)
# ----------------------------
def load_env():
    if getattr(sys, "frozen", False):  # Running from .exe
        base_path = Path(sys.executable).parent
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
# Get System Info
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

    disk = psutil.disk_usage('/')
    info["Disk Total (GB)"] = round(disk.total / (1024 ** 3), 2)
    info["Disk Used (%)"] = disk.percent

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
    output_box.delete(1.0, END)
    output_box.insert(END, "📋 SYSTEM INFORMATION:\n\n")
    for key, value in info.items():
        line = f"{key}: {value}\n"
        output_box.insert(END, line)
        logging.info(line)

# ----------------------------
# Send Email Report
# ----------------------------
def send_email_report():
    email_sender = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_receiver = email_sender

    try:
        with open("system_info.log", "r") as f:
            log_content = f.read()
    except FileNotFoundError:
        output_box.insert(END, "\n❌ Log file not found. Click 'Get System Info' first.\n")
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
        output_box.insert(END, "\n✅ Email sent successfully!\n")
    except Exception as e:
        output_box.insert(END, f"\n❌ Failed to send email: {e}\n")

# ----------------------------
# Live Resource Monitor
# ----------------------------
def update_live_stats():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    live_label.config(
        text=f"💻 CPU: {cpu}%   |   🧠 RAM: {ram}%   |   💾 Disk: {disk}%"
    )

    window.after(1000, update_live_stats)

# ----------------------------
# GUI Setup
# ----------------------------
window = Tk()
window.title("System Info Collector")
window.geometry("700x550")
window.configure(bg="black")

# Live Resource Label
live_label = Label(window, text="", bg="black", fg="white", font=("Arial", 12))
live_label.pack(pady=10)

# Output box
output_box = Text(window, height=20, width=85, bg="black", fg="white", insertbackground="white")
output_box.pack(pady=10)

# Buttons
Button(window, text="🧠 Get System Info", command=display_and_log_info,
       bg="#333", fg="white", activebackground="#444").pack(pady=5)
Button(window, text="📧 Send Email Report", command=send_email_report,
       bg="#333", fg="white", activebackground="#444").pack(pady=5)

# Start live stats update
update_live_stats()

window.mainloop()
