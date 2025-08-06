import json
import os
import matplotlib.pyplot as plt

def generate_language_pie_chart(username):
    data_path = f"Github/data/{username}.json"
    output_dir = "Github/output/Graphics"
    os.makedirs(output_dir, exist_ok=True)

    # Load GitHub data
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Aggregate language usage
    language_totals = {}
    for repo in data.get("repos", []):
        languages = repo.get("all_languages", {})
        for lang, bytes_of_code in languages.items():
            language_totals[lang] = language_totals.get(lang, 0) + bytes_of_code

    # If no languages found
    if not language_totals:
        print("⚠️ No language data found.")
        return

    # Sort and prepare data
    sorted_langs = dict(sorted(language_totals.items(), key=lambda item: item[1], reverse=True))
    labels = list(sorted_langs.keys())
    sizes = list(sorted_langs.values())

    # Create Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")  # Equal aspect ratio = circle
    plt.title(f"{username}'s Language Usage", fontsize=14)

    # Save to file
    chart_path = os.path.join(output_dir, f"{username}_language_chart.png")
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    print(f"✅ Language pie chart saved to {chart_path}")
