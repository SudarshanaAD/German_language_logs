import os
import datetime
import requests

DUOLINGO_USERNAME = "Sudarshan2112"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

# ✅ Correct API-style endpoint for user data
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
    print(response.text[:500])  # show first 500 chars for debugging
    exit(1)

user_list = data.get("users", [])
if not user_list:
    print(f"[ERROR] Profile '{DUOLINGO_USERNAME}' not found.")
    exit(1)

# ✅ Extract statistics
user_info = user_list[0]
streak = user_info.get("streak", 0)
total_xp = user_info.get("totalXp", 0)
print(f"[DEBUG 3] Parsing confirmation -> Streak: {streak}, XP: {total_xp}")

# ✅ Generate Markdown log
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
