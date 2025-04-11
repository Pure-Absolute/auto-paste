import os
import time
from threading import Thread

TEXT_FILE = "/home/agis/Desktop/my code/AFK paste/string.txt"
TYPE_DELAY = 0.06
MINIMUM_INTERVAL = 5
START_DELAY = 1

store["afk_running"] = True
store["afk_paused"] = False
store["afk_line_index"] = 0  # <-- Reset to beginning on fresh start

def type_text(text):
    for char in text:
        keyboard.send_keys(char)
        time.sleep(TYPE_DELAY)

def afk_loop():
    if not os.path.exists(TEXT_FILE):
        keyboard.send_keys("Text file not found.")
        store["afk_running"] = False
        return

    with open(TEXT_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        keyboard.send_keys("No lines to type.")
        store["afk_running"] = False
        return

    line_index = 0

    while store.get("afk_running", False) and line_index < len(lines):
        if store.get("afk_paused", False):
            time.sleep(0.5)
            continue

        current_line = lines[line_index]
        time.sleep(START_DELAY)
        type_text(current_line)
        time.sleep(5)
        keyboard.send_keys("<enter>")

        line_index += 1
        store["afk_line_index"] = line_index

        if line_index >= len(lines):
            keyboard.send_keys("AFK script finished.")
            store["afk_running"] = False
            break

        time.sleep(max(MINIMUM_INTERVAL, len(current_line) * TYPE_DELAY))

thread = Thread(target=afk_loop)
thread.start()
