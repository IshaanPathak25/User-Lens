import requests
import os
import json
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime, timedelta

GITHUB_API_BASE = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
} if GITHUB_TOKEN else {}

def fetch_user_profile(username):
    url = f"{GITHUB_API_BASE}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch profile: {response.status_code} - {response.text}")
    return response.json()

def fetch_user_repos(username):
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

def fetch_repo_languages(full_name):
    url = f"{GITHUB_API_BASE}/repos/{full_name}/languages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠️ Could not fetch languages for {full_name}")
        return {}

def fetch_contribution_calendar(username):
    all_daily_contributions = []
    total_contributions_sum = 0

    today = datetime.today()
    current_to = today
    current_from = today - timedelta(days=365)

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
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

    while True:
        variables = {
            "login": username,
            "from": current_from.isoformat(),
            "to": current_to.isoformat()
        }
        response = requests.post(
            GITHUB_GRAPHQL_URL,
            headers=HEADERS,
            json={"query": query, "variables": variables}
        )

        if response.status_code != 200:
            raise Exception(f"GraphQL error: {response.status_code} - {response.text}")

        data = response.json()
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

        daily_contribs = [
            {
                "date": day["date"],
                "count": day["contributionCount"]
            }
            for week in weeks
            for day in week["contributionDays"]
        ]

        if not daily_contribs or all(d["count"] == 0 for d in daily_contribs):
            break

        all_daily_contributions.extend(daily_contribs)
        total_contributions_sum += sum(d["count"] for d in daily_contribs)

        current_to = current_from
        current_from = current_from - timedelta(days=365)

        if current_from.year < 2008:
            break

    all_daily_contributions = {d["date"]: d["count"] for d in all_daily_contributions}
    all_daily_contributions = [
        {"date": k, "count": v} for k, v in sorted(all_daily_contributions.items())
    ]

    return total_contributions_sum, all_daily_contributions

def fetch_pull_requests_count(username):
    url = f"{GITHUB_API_BASE}/search/issues?q=author:{username}+type:pr"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("total_count", 0)
    else:
        print(f"⚠️ Could not fetch pull requests for {username}")
        return 0

def fetch_issues_count(username):
    url = f"{GITHUB_API_BASE}/search/issues?q=author:{username}+type:issue"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("total_count", 0)
    else:
        print(f"⚠️ Could not fetch issues for {username}")
        return 0

def group_commits_by_month(daily_contributions):
    monthly = defaultdict(int)
    for entry in daily_contributions:
        dt = datetime.strptime(entry["date"], "%Y-%m-%d")
        month_key = dt.strftime("%Y-%m")
        monthly[month_key] += entry["count"]
    return dict(sorted(monthly.items(), key=lambda x: x[0]))

def get_basic_github_data(username):
    profile = fetch_user_profile(username)
    repos = fetch_user_repos(username)
    total_contributions, daily_contributions = fetch_contribution_calendar(username)

    monthly_contributions = group_commits_by_month(daily_contributions)

    # Free memory: remove daily_contributions now that monthly is computed
    del daily_contributions  

    stars_total = sum(repo["stargazers_count"] for repo in repos)
    forks_total = sum(repo["forks_count"] for repo in repos)
    pull_requests_total = fetch_pull_requests_count(username)
    issues_total = fetch_issues_count(username)

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
        "contribution_calendar": {
            "total_contributions": total_contributions
        },
        "monthly_contributions": monthly_contributions,
        "total_stars": stars_total,
        "total_forks": forks_total,
        "total_pull_requests": pull_requests_total,
        "total_issues": issues_total,
        "repos": [
            {
                "name": repo["name"],
                "description": repo["description"],
                "language": repo["language"],
                "all_languages": fetch_repo_languages(repo["full_name"]),
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "html_url": repo["html_url"]
            }
            for repo in repos
        ]
    }

def save_github_data(username):
    print(f"📥 Fetching GitHub data for user: {username}...")
    user_data = get_basic_github_data(username)

    os.makedirs("Github/data", exist_ok=True)
    filepath = f"Github/data/{username}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2)

    print(f"✅ GitHub data saved to {filepath}")