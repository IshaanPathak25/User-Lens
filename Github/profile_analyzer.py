import json
import os
import cohere
import textwrap
from dotenv import load_dotenv

# Load API Key securely
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
client = cohere.Client(COHERE_API_KEY)

WRAP_WIDTH = 120  # Max characters per line

def format_profile_output(raw_text):
    """Format output with markdown-style headers and wrapped content."""
    lines = raw_text.strip().splitlines()
    formatted_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append("")
        elif stripped.endswith(":") and len(stripped.split()) < 5:
            # Markdown-style heading
            formatted_lines.append(f"\n### {stripped.rstrip(':')}\n")
        else:
            wrapped = textwrap.fill(stripped, width=WRAP_WIDTH)
            formatted_lines.append(wrapped)

    return "\n".join(formatted_lines)

def analyze_github_profile(username):
    print("🔍 Analyzing GitHub profile with Cohere...")

    filepath = f"Github/data/{username}.json"
    if not os.path.exists(filepath):
        print(f"❌ Data file not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    bio = data.get("bio", "N/A")
    location = data.get("location", "N/A")

    # Prepare repo summaries
    repo_summaries = []
    for repo in data.get("repos", [])[:10]:  # Limit to 10 for safety
        summary = (
            f"- **{repo['name']}**: {repo.get('description') or 'No description'}"
            f" | ⭐ {repo['stars']} | 🍴 {repo['forks']} | 📝 Language: {repo['language'] or 'N/A'}"
        )
        repo_summaries.append(summary)

    prompt = f"""
You are an expert GitHub profile analyst. Based on the GitHub user's activity and public repositories, generate a detailed profile including these sections:

## Name (Use GitHub username only: {username})
## Bio
## Location
## Development Interests
## Open Source Involvement
## Technical Strengths
## Collaboration Style
## Notable Repositories (summarize briefly with impact)
## Summary

GitHub Bio: {bio}
Location: {location}

Repositories:
{chr(10).join(repo_summaries)}
""".strip()

    try:
        response = client.generate(
            model="command-r-plus",
            prompt=prompt,
            temperature=0.6,
            max_tokens=1500
        )
        raw_output = response.generations[0].text.strip()

        if not raw_output:
            print("❌ Empty response from Cohere.")
            return

        formatted = format_profile_output(raw_output)

        os.makedirs("Github/output", exist_ok=True)
        output_path = f"Github/output/{username}_github_profile.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"✅ GitHub profile analysis saved to {output_path}")
    except Exception as e:
        print(f"❌ Cohere API error: {e}")