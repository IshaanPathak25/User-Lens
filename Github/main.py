import re
import subprocess
import os
from .profile_analyzer import analyze_github_profile
from .visual_generator import generate_visual_persona

def extract_username_from_url(url):
    match = re.match(r"https?://github\.com/([A-Za-z0-9-]+)", url)
    if not match:
        raise ValueError("❌ Invalid GitHub profile URL.")
    return match.group(1)

def main():
    print("👋 Welcome to GitHub Profile Analyzer!")
    url = input("🔗 Enter GitHub profile URL: ").strip()

    if not url.startswith("https://github.com/"):
        print("❌ Invalid GitHub profile URL format.")
        return

    # try:
    #     username = extract_username_from_url(url)
    #     save_github_data(username)
    #     analyze_github_profile(username)
    # except Exception as e:
    #     print(f"❌ Error: {e}")
    
    username = extract_username_from_url(url)
    print(f"📥 Scraping data for: {username}...")

    result = subprocess.run([os.sys.executable, "Github/github_scraper.py", url])

    if result.returncode != 0:
        print("❌ Failed to scrape GitHub data.")
        return

    print(f"🧠 Generating persona for: {username}...")
    analyze_github_profile(username)

    # 🔁 Ask if user wants a visual persona
    choice = input("🎨 Would you like to generate a visual persona as well? (y/n): ").lower().strip()
    if choice == 'y':
        print("🖼️ Generating visual persona...")
        generate_visual_persona(username)
        print(f"✅ Visual persona saved as: output/{username}_persona.png")
    else:
        print("👋 Exiting without visual persona.")

if __name__ == "__main__":
    main()

def run_github_pipeline(username):
    from .github_scraper import save_github_data
    save_github_data(username)
    
    from .profile_analyzer import analyze_github_profile
    analyze_github_profile(username)
    
    from .visual_generator import generate_visual_persona
    generate_visual_persona(username)
    
    # from visualizer import generate_all_charts
    # generate_all_charts(username)
