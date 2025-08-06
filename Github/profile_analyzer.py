import json
import os
import cohere
import textwrap
import re  # Added for regex parsing
from dotenv import load_dotenv

# Load API Key securely
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
client = cohere.Client(COHERE_API_KEY)

WRAP_WIDTH = 155  # Max characters per line

def format_profile_output(raw_text, username):
    # Expected sections for GitHub persona
    sections = [
        "Name", "Bio", "Location", "Development Interests", "Open Source Involvement",
        "Technical Strengths", "Collaboration Style", "Notable Repositories", "Summary"
    ]
    section_map = {section: "" for section in sections}

    for section in sections:
        # Matches markdown headers like "## Bio" or "# Bio"
        pattern = re.compile(
            rf"#+\s*{re.escape(section)}\s*\n(.*?)(?=\n#+\s*\w+|\Z)",
            re.DOTALL | re.IGNORECASE
        )
        match = pattern.search(raw_text)
        if match:
            section_map[section] = match.group(1).strip()

    # Always use the GitHub username in the "Name" field
    section_map["Name"] = username

    return section_map


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

## Name
(Use GitHub username only: {username})

## Bio

## Location

## Development Interests

## Open Source Involvement

## Technical Strengths

## Collaboration Style

## Notable Repositories
(Summarize briefly with impact)

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
        #print("📄 Raw Cohere output:\n", raw_output)

        if not raw_output:
            print("❌ Empty response from Cohere.")
            return

        formatted = format_profile_output(raw_output, username)

        os.makedirs("Github/output/Script", exist_ok=True)
        output_path = f"Github/output/Script/{username}_github_profile.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for key, value in formatted.items():
                f.write(f"{key}:\n{value.strip()}\n\n")

        print(f"✅ GitHub profile analysis saved to {output_path}")
    except Exception as e:
        print(f"❌ Cohere API error: {e}")
