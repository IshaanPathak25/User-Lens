import re
from .github_scraper import save_github_data
from .profile_analyzer import analyze_github_profile

def extract_username_from_url(url):
    match = re.match(r"https?://github\.com/([A-Za-z0-9-]+)", url)
    if not match:
        raise ValueError("❌ Invalid GitHub profile URL.")
    return match.group(1)

def main():
    print("👋 Welcome to GitHub Profile Analyzer!")
    url = input("🔗 Enter GitHub profile URL: ").strip()

    try:
        username = extract_username_from_url(url)
        save_github_data(username)
        analyze_github_profile(username)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

def run_github_pipeline(username):
    from .github_scraper import save_github_data
    from .profile_analyzer import analyze_github_profile
    # from visualizer import generate_all_charts

    save_github_data(username)
    analyze_github_profile(username)
    # generate_all_charts(username)
