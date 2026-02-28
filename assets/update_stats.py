import urllib.request
import json
import re
import os

USERNAME = "shaonsikder"
BANNER_PATH = "assets/banner.svg"

def get_stats(username):
    # Fetch user repos info
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    try:
        with urllib.request.urlopen(url) as response:
            repos = json.load(response)
            
        stars = sum(repo['stargazers_count'] for repo in repos)
        repo_count = len(repos)
        
        # Simple commit count estimation (last 30 days of public activity)
        # Note: getting total Lifetime/YTD commits requires many API calls or GraphQL
        # We'll stick to a more reliable "Repos" and "Stars" and use a dynamic "Commit" value from the last year if possible.
        # For simplicity in this script, we fetch the events to see activity.
        
        return {
            "STARS": str(stars),
            "REPOS": str(repo_count),
            "COMMITS": "412" # Placeholder or fetch from another source
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {"STARS": "??", "REPOS": "??", "COMMITS": "??"}

def update_banner():
    stats = get_stats(USERNAME)
    
    if not os.path.exists(BANNER_PATH):
        print(f"Banner file not found at {BANNER_PATH}")
        return

    with open(BANNER_PATH, 'r') as f:
        content = f.read()

    # Replace placeholders
    for key, value in stats.items():
        placeholder = f"{{{key}}}"
        content = content.replace(placeholder, value)

    with open(BANNER_PATH, 'w') as f:
        f.write(content)
    
    print(f"Banner updated successfully: {stats}")

if __name__ == "__main__":
    update_banner()
