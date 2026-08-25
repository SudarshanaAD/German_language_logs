import os
import datetime
import requests

DUOLINGO_USERNAME = 'Sudarshan2112' 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Fetch live metrics from the Duolingo API
url = f"https://duolingo.com{DUOLINGO_USERNAME}"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"[ERROR] Failed to connect to Duolingo. Code: {response.status_code}")
    exit(1)

data = response.json()
user_list = data.get('users', [])

if not user_list:
    print(f"[ERROR] Profile '{DUOLINGO_USERNAME}' not found.")
    exit(1)

user_info = user_list[0]
streak = user_info.get('streak', 0)
total_xp = user_info.get('totalXp', 0)

# 2. Date parsing variables
today_dash = datetime.datetime.now().strftime("%Y-%m-%d")
today_text = datetime.datetime.now().strftime("%d %b %Y")
weekday_name = datetime.datetime.now().strftime("%A")

# 3. Create individual milestone diary markdown logs
log_dir = "German_language_logs"
os.makedirs(log_dir, exist_ok=True)
diary_path = os.path.join(log_dir, f"{today_dash}.md")

diary_content = f"""# Duolingo Progress – {today_text}
* **XP Score:** {total_xp} Duolingo XP
* **Streak:** {streak} days 🔥
* **Notes:** Automated daily check-in logs.
"""
with open(diary_path, "w", encoding="utf-8") as f:
    f.write(diary_content)

# 4. Handle structural weekly rolling metrics tracking ledger
weekly_ledger_path = os.path.join(log_dir, "weekly_rolling_tracker.txt")
history_lines = []

if os.path.exists(weekly_ledger_path):
    with open(weekly_ledger_path, "r", encoding="utf-8") as f:
        history_lines = [line.strip() for line in f.readlines() if line.strip()]

# Append today's statistics log snapshot entry
history_lines.append(f"{today_text} ({weekday_name})|{total_xp}")

# Keep a maximum rolling historical window of the last 7 entries
if len(history_lines) > 7:
    history_lines = history_lines[-7:]

with open(weekly_ledger_path, "w", encoding="utf-8") as f:
    f.write("\n".join(history_lines))

# 5. Build dynamic table layout strings for your README
table_rows = ""
for i in range(1, len(history_lines)):
    try:
        prev_date, prev_xp = history_lines[i-1].split("|")
        curr_date, curr_xp = history_lines[i].split("|")
        day_gained = int(curr_xp) - int(prev_xp)
        if day_gained < 0: day_gained = 0 # Safety reset for edge cases
        table_rows += f"| {curr_date.split(' (')[0]} | {curr_xp} XP | +{day_gained} XP |\n"
    except Exception:
        continue

if not table_rows:
    table_rows = f"| {today_text} | {total_xp} XP | Logging initialization... |\n"

# 6. Overwrite the main README file completely to include the stats interface dashboard
readme_content = f"""# German Language Tracking Logs 🇩🇪

This repository automatically maintains my weekly progress tracking ledger from Duolingo. It dynamically updates metrics using custom Python-driven GitHub Actions.

---

### 📊 Live Metric Tracker Dashboard

| Current Streak 🔥 | Total Accumulated Volume 📈 | Last Dynamic Run Update ⏱️ |
| :--- | :--- | :--- |
| **{streak} Days Active** | **{total_xp} Total XP** | {today_text} ({weekday_name}) |

---

### 📅 Weekly XP Generation Log Summary

| Day / Date | Accumulated Level Baseline | Net Daily Performance |
| :--- | :--- | :--- |
{table_rows}
---
*Automated reporting generated via background scripts.*
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("[SUCCESS] Layout updating complete.")
