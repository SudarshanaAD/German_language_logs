import os
import datetime
from duolingo import Duolingo

# Fetch secure environment variables
username = os.getenv('DUOLINGO_USERNAME')
password = os.getenv('DUOLINGO_PASSWORD')

# Log in to the unofficial Duolingo API wrapper
lingo = Duolingo(username, password)

# Fetch current target statistics
streak = lingo.get_streak_info()['site_streak']
user_data = lingo.get_user_data()
total_xp = user_data['total_xp']

# Format today's dates for file naming conventions
today_dash = datetime.datetime.now().strftime("%Y-%m-%d")
today_text = datetime.datetime.now().strftime("%d %b %Y")

# Build target directory path if it doesn't exist
log_dir = "German_language_logs"
os.makedirs(log_dir, exist_ok=True)
file_path = os.path.join(log_dir, f"{today_dash}.md")

# Write out the standardized Markdown file structure
markdown_content = f"""# Duolingo Progress – {today_text}

* **XP Score:** {total_xp} Duolingo XP
* **Streak:** [{streak}]
* **Notes:** Automated daily check-in logs.
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Successfully generated language progress log: {file_path}")
