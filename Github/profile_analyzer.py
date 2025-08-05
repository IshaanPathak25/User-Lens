import json
import os
import cohere
import textwrap
from dotenv import load_dotenv

# Load API Key securely
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
client = cohere.Client(COHERE_API_KEY)

WRAP_WIDTH = 155  # Max characters per line

# def format_profile_output(raw_text):
#     """Format output with 'Key:' on its own line followed by wrapped content, matching Reddit persona style."""
#     lines = raw_text.strip().splitlines()
#     formatted_lines = []
#     current_section = None

#     for line in lines:
#         stripped = line.strip()
#         if not stripped:
#             continue
#         # Detect section headings: e.g., "Bio:", "Summary:", etc.
#         if stripped.endswith(":") and len(stripped.split()) < 5:
#             current_section = stripped.rstrip(":")
#             formatted_lines.append(f"{current_section}:\n")
#         else:
#             wrapped = textwrap.fill(stripped, width=WRAP_WIDTH)
#             formatted_lines.append(wrapped + "\n")

#     return "\n".join(formatted_lines)

def format_profile_output(raw_text, username):
    sections = {
        "Name": "",
        "Bio": "",
        "Location": "",
        "Development Interests": "",
        "Open Source Involements": "",
        "Technical Strengths": "",
        "Collaboration Style": "",
        "Notable Repositories": "",
        "Summary": ""
    }

    current = None
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        for key in list(sections.keys())[1:]:  # Skip "Name"
            if line.lower().startswith(f"{key.lower()}:"):
                current = key
                line = line[len(key)+1:].strip()
                sections[current] += line + "\n"
                break
        else:
            if current:
                sections[current] += line + "\n"

    return sections


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

- Name (Use GitHub username only: {username})
- Bio
- Location
- Development Interests
- Open Source Involvement
- Technical Strengths
- Collaboration Style
- Notable Repositories (summarize briefly with impact)
- Summary

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

        os.makedirs("Github/output/Script", exist_ok=True)
        output_path = f"Github/output/Script/{username}_github_profile.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"✅ GitHub profile analysis saved to {output_path}")
    except Exception as e:
        print(f"❌ Cohere API error: {e}")