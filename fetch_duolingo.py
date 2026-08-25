import os
import datetime
import requests

DUOLINGO_USERNAME = "Sudarshan2112"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

# ✅ Correct JSON endpoint
url = f"https://www.duolingo.com/2017-06-30/users?username={DUOLINGO_USERNAME}"
print(f"[DEBUG 1] Target URL verification: {url}")

response = requests.get(url, headers=headers)
print(f"[DEBUG 2] Connection code: {response.status_code}")

if response.status_code != 200:
    print("[ERROR] Connection to API endpoint failed.")
    exit(1)

try:
    data = response.json()
except ValueError:
    print("[ERROR] Response was not JSON. Raw output:")
    print(response.text[:500])
    exit(1)

user_list = data.get("users", [])
if not user_list:
    print(f"[ERROR] Profile '{DUOLINGO_USERNAME}' not found.")
    exit(1)

# ✅ Extract stats
user_info = user_list[0]
streak = user_info.get("streak", 0)
total_xp = user_info.get("totalXp", 0)
print(f"[DEBUG 3] Parsing confirmation -> Streak: {streak}, XP: {total_xp}")

# ✅ Daily log file
today_dash = datetime.datetime.now().strftime("%Y-%m-%d")
today_text = datetime.datetime.now().strftime("%d %b %Y")

log_dir = "German_language_logs"
os.makedirs(log_dir, exist_ok=True)
file_path = os.path.join(log_dir, f"{today_dash}.md")

markdown_content = f"""# Duolingo Progress – {today_text}

* **XP Score:** {total_xp} Duolingo XP
* **Streak:** {streak} days 🔥
* **Notes:** Automated daily check-in logs.
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"[SUCCESS] File generated: {file_path}")

# ✅ Update README.md with live streak badge
readme_path = os.path.join(log_dir, "README.md")
badge_url = f"https://img.shields.io/badge/Duolingo_Streak-{streak}_days-brightgreen?logo=duolingo"

readme_content = f"""# German_language_logs

This repository tracks my weekly progress in learning German from A1 level, including vocabulary logs, grammar notes, and reflections.

![Duolingo Streak Badge]({badge_url})

## Current Stats
- **XP:** {total_xp}
- **Streak:** {streak} days 🔥
"""

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"[SUCCESS] README updated with streak badge.")

# ✅ Weekly summary chart (XP gained per day)
summary_path = os.path.join(log_dir, "weekly_summary.md")

# Load past 7 logs
xp_data = []
for i in range(7):
    day = datetime.datetime.now() - datetime.timedelta(days=i)
    fname = os.path.join(log_dir, f"{day.strftime('%Y-%m-%d')}.md")
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            content = f.read()
            # crude parse: look for XP line
            for line in content.splitlines():
                if "XP Score:" in line:
                    xp_val = int(line.split()[2])  # extract XP number
                    xp_data.append((day.strftime("%d %b"), xp_val))

# Sort oldest → newest
xp_data = sorted(xp_data, key=lambda x: datetime.datetime.strptime(x[0], "%d %b"))

# Build summary table
summary_table = "| Date | XP |\n|------|----|\n"
for date, xp in xp_data:
    summary_table += f"| {date} | {xp} |\n"

weekly_content = f"""# Weekly XP Summary

This chart shows total XP gained each day over the past week.

{summary_table}
"""

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(weekly_content)

print(f"[SUCCESS] Weekly summary generated: {summary_path}")
