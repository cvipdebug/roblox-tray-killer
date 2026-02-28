# Roblox Tray Killer

**Stop Roblox from cluttering your system tray!**  
Roblox has added a new `--launch-to-tray` feature. When you close the game, the client stays in the tray. Re-open the game and now you have **two** Roblox instances running in the background. This script automatically detects and kills those hidden tray processes so your tray stays clean.

---

## ✨ Features

- **Auto-kill on detection** – Scans every 3 seconds for `RobloxPlayerBeta.exe --launch-to-tray`
- **System Tray App** – Lives in your tray with a clean icon and live kill counter
- **Toggle Monitoring** – Pause/resume with one click
- **Persistent Kill Counter** – Remembers your total kills even after restart
- **Detailed Logging** – Every kill is logged with timestamp, PID, and full command line
- **Desktop Notifications** – You’ll see a toast every time Roblox gets blocked
- **.pyw version** – Runs completely hidden (no console window)

---

## 📸 Preview

- Tray icon shows live kill count
- Right-click menu: “Kills: X”, Toggle Monitoring, Exit

---

## 🛠️ Installation

1. **Install Python** (3.8+ recommended) → [python.org](https://www.python.org/downloads/)
2. **Clone or download** this repository
3. **Install dependencies** (one-time):

```bash
pip install psutil pystray pillow
