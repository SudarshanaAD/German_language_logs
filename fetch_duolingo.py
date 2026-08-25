import os
import datetime
import requests

# Put your exact Duolingo username here
DUOLINGO_USERNAME = 'Sudarshan2112' 

# Set up headers to look like a standard web browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Fetch raw public profile information from Duolingo's API endpoint
url = f"https://duolingo.com{DUOLINGO_USERNAME}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    user_info = data['users'][0]
    
    # Extract matching metrics
    streak = user_info.get('streak', 0)
    total_xp = user_info.get('totalXp', 0)
    
    # Format calendar dates
    today_dash = datetime.datetime.now().strftime("%Y-%m-%d")
    today_text = datetime.datetime.now().strftime("%d %b %Y")
    
    # Create target storage directory
    log_dir = "German_language_logs"
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, f"{today_dash}.md")
    
    # Build your custom file template
    markdown_content = f"""# Duolingo Progress – {today_text}

* **XP Score:** {total_xp} Duolingo XP
* **Streak:** {streak} days 🔥
* **Notes:** Automated daily check-in logs.
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"Successfully generated language progress log: {file_path}")
else:
    print(f"Failed to fetch data from Duolingo. Status code: {response.status_code}")
    exit(1)
