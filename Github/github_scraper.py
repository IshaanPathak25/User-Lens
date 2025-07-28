import requests
import os
import json
from dotenv import load_dotenv

GITHUB_API_BASE = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
} if GITHUB_TOKEN else {}

def fetch_user_profile(username):
    """Fetch basic profile information for a given GitHub username."""
    url = f"{GITHUB_API_BASE}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch profile: {response.status_code} - {response.text}")
    return response.json()

def fetch_user_repos(username):
    """Fetch list of public repositories for a given GitHub user."""
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repositories: {response.status_code} - {response.text}")
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def fetch_contribution_calendar(username):
    """Fetch GitHub contribution calendar data (last year)."""
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    variables = {"login": username}
    response = requests.post(
        GITHUB_GRAPHQL_URL,
        headers=HEADERS,
        json={"query": query, "variables": variables}
    )

    if response.status_code != 200:
        raise Exception(f"GraphQL error: {response.status_code} - {response.text}")

    data = response.json()
    calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return {
        "total_contributions": calendar["totalContributions"],
        "daily_contributions": [
            {
                "date": day["date"],
                "count": day["contributionCount"]
            }
            for week in calendar["weeks"]
            for day in week["contributionDays"]
        ]
    }

def get_basic_github_data(username):
    """Returns summarized GitHub data for a user."""
    profile = fetch_user_profile(username)
    repos = fetch_user_repos(username)
    calendar = fetch_contribution_calendar(username)

    return {
        "username": username,
        "name": profile.get("name") or username,
        "bio": profile.get("bio"),
        "location": profile.get("location"),
        "public_repos_count": profile.get("public_repos"),
        "followers": profile.get("followers"),
        "following": profile.get("following"),
        "profile_url": profile.get("html_url"),
        "avatar_url": profile.get("avatar_url"),
        "contribution_calendar": calendar,
        "repos": [
            {
                "name": repo["name"],
                "description": repo["description"],
                "language": repo["language"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "html_url": repo["html_url"]
            }
            for repo in repos
        ]
    }

def save_github_data(username):
    """Fetch and save GitHub data to data/{username}.json"""
    print(f"📥 Fetching GitHub data for user: {username}...")
    user_data = get_basic_github_data(username)

    os.makedirs("Github/data", exist_ok=True)
    filepath = f"Github/data/{username}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2)

    print(f"✅ GitHub data saved to {filepath}")
