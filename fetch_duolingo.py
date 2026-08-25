import os
import datetime
import requests

DUOLINGO_USERNAME = 'Sudarshan2112' 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = f"https://duolingo.com{DUOLINGO_USERNAME}"
print(f"[DEBUG 1] Attempting to reach URL: {url}")

response = requests.get(url, headers=headers)
print(f"[DEBUG 2] Connection Status Code: {response.status_code}")

if response.status_code != 200:
    print("[ERROR] Failed to connect to Duolingo.")
    exit(1)

data = response.json()
user_list = data.get('users', [])
print(f"[DEBUG 3] Type of data['users']: {type(user_list)} (Length: {len(user_list)})")

if not user_list or len(user_list) == 0:
    print(f"[ERROR] User '{DUOLINGO_USERNAME}' not found.")
    exit(1)

# Safely extract from the profile object list
user_info = user_list[0]
streak = user_info.get('streak', 0)
total_xp = user_info.get('totalXp', 0)
print(f"[DEBUG 4] Extracted Stats -> Streak: {streak}, XP: {total_xp}")

today_dash = datetime.datetime.now().strftime("%Y-%m-%d")
today_text = datetime.datetime.now().strftime("%d %b %Y")

log_dir = "German_language_logs"
os.makedirs(log_dir, exist_ok=True)
file_path = os.path.join(log_dir, f"{today_dash}.md")
print(f"[DEBUG 5] Target file destination path: {file_path}")

markdown_content = f"""# Duolingo Progress – {today_text}

* **XP Score:** {total_xp} Duolingo XP
* **Streak:** {streak} days 🔥
* **Notes:** Automated daily check-in logs.
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)
    
print(f"[SUCCESS] Log file successfully written to: {file_path}")

