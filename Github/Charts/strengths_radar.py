import json
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_radar_chart(username):
    # Paths
    json_path = f"GitHub/data/{username}.json"
    output_dir = "GitHub/output/Graphics"
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract metrics directly from JSON
    stars = data.get("total_stars", 0)
    forks = data.get("total_forks", 0)
    pull_requests = data.get("total_pull_requests", 0)
    issues = data.get("total_issues", 0)
    total_contributions = data.get("contribution_calendar", {}).get("total_contributions", 0)

    # Labels & values
    labels = ["Stars", "Forks", "Pull Requests", "Issues", "Contributions"]
    values = [stars, forks, pull_requests, issues, total_contributions]

    # Close radar chart loop
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)

    # Create radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)

    # Labels & formatting
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title(f"{username} - GitHub Activity Radar", size=16, weight='bold', pad=20)
    ax.set_yticklabels([])  # Hide radial labels for cleaner look

    # Save chart
    output_path = os.path.join(output_dir, f"{username}_radar_chart.png")
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[INFO] Radar chart saved to {output_path}")


# Example usage for manual testing
# if __name__ == "__main__":
#     generate_radar_chart("YOUR_GITHUB_USERNAME")