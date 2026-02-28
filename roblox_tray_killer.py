import psutil
import time
import threading
import sys
import os
import datetime
from pystray import Icon, Menu, MenuItem
from PIL import Image

# ======================
# CONFIG
# ======================
ROBLOX_EXE = "RobloxPlayerBeta.exe"
CHECK_INTERVAL = 3  # seconds

BASE_DIR = os.path.dirname(sys.argv[0])
LOG_FILE = os.path.join(BASE_DIR, "roblox_kill_log.txt")
KILL_COUNT_FILE = os.path.join(BASE_DIR, "kill_count.txt")
ICON_FILE = os.path.join(BASE_DIR, "roblox_block.ico")

# ======================
# GLOBAL STATE
# ======================
MONITORING = True
kill_count = 0
icon = None

# ======================
# UTILITIES
# ======================
def load_kill_count():
    try:
        with open(KILL_COUNT_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_kill_count(count):
    with open(KILL_COUNT_FILE, "w") as f:
        f.write(str(count))

def log_kill(proc):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n"
            f"Process: {proc.info['name']}\n"
            f"PID: {proc.info['pid']}\n"
            f"Cmd: {' '.join(proc.info['cmdline'])}\n"
            f"{'-'*40}\n"
        )

def load_icon():
    return Image.open(ICON_FILE)

# ======================
# TRAY MENU
# ======================
def build_menu():
    return Menu(
        MenuItem(
            lambda text: f"Kills: {kill_count}",
            lambda icon, item: None,
            enabled=False
        ),
        Menu.SEPARATOR,
        MenuItem("Toggle Monitoring", toggle_monitoring),
        MenuItem("Exit", exit_app)
    )

# ======================
# ACTIONS
# ======================
def toggle_monitoring(icon_, item):
    global MONITORING
    MONITORING = not MONITORING
    icon_.notify(
        "Monitoring Enabled" if MONITORING else "Monitoring Paused",
        "Roblox Tray Killer"
    )

def exit_app(icon_, item):
    icon_.stop()
    sys.exit()

# ======================
# WATCHDOG THREAD
# ======================
def find_and_kill():
    global kill_count, icon

    while True:
        if MONITORING:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] == ROBLOX_EXE:
                        cmdline = " ".join(proc.info['cmdline'])
                        if "--launch-to-tray" in cmdline:
                            log_kill(proc)
                            proc.terminate()

                            kill_count += 1
                            save_kill_count(kill_count)

                            if icon:
                                icon.title = f"Roblox Tray Killer — Kills: {kill_count}"
                                icon.menu = build_menu()
                                icon.notify(
                                    "Roblox was killed",
                                    f"launch-to-tray blocked (Total: {kill_count})"
                                )

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        time.sleep(CHECK_INTERVAL)

# ======================
# MAIN
# ======================
def main():
    global icon, kill_count

    kill_count = load_kill_count()

    icon = Icon(
        "Roblox Tray Killer",
        load_icon(),
        menu=build_menu()
    )

    icon.title = f"Roblox Tray Killer — Kills: {kill_count}"

    thread = threading.Thread(target=find_and_kill, daemon=True)
    thread.start()

    icon.run()

if __name__ == "__main__":
    main()