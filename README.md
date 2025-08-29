# 📊 System Info Collector

A Python project that collects **system information** such as OS details, CPU, memory, disk usage, and network info.  
It can log the data to a file and send it to your email (via Gmail App Password).  
Also includes an optional **Tkinter GUI** version and can be converted into an `.exe` for easy sharing.

---

## 🚀 Features

- Collects OS, CPU, RAM, Disk, and Network info
- Saves info to `system_info.log`
- Sends info to your email automatically
- Optional Tkinter-based GUI
- Can be built as `.exe` (Windows executable)

---

## 📂 Project Structure

system_info_collector/
│── system_info.py # Console version
│── system_info_gui.py # GUI version
│── requirements.txt # Python dependencies
│── .env.sample # Template for email credentials
│── .gitignore # Ignore unnecessary files in GitHub
│── README.md # Project documentation

---

## ⚙️ Requirements

- Python **3.10+**
- Gmail account with **App Password** enabled
- Modules from `requirements.txt`

---

## 📥 Installation

**1️⃣ Clone the repository**

```bash
git clone https://github.com/your-username/system_info_collector.git
cd system_info_collector

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ ### Setting up Environment Variables

1. Copy the `.env.sample` file to a new file named `.env`:

2. Open `.env` and replace the placeholders with your real details:

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

▶️ Running the Project

Console Version:
python system_info.py

GUI Version:
python system_info_gui.py

💻 Build as .exe (Optional)

If you want to share the project without requiring Python installed:

Console version:
pyinstaller --onefile --hidden-import=dotenv system_info.py

GUI version:
pyinstaller --onefile --hidden-import=dotenv system_info_gui.py