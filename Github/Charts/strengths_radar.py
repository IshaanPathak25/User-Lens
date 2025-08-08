import json
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_radar_chart_with_percentages(username):
    # Paths
    json_path = f"GitHub/data/{username}.json"
    output_dir = "GitHub/output/Graphics"
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract raw metrics
    stars = data.get("total_stars", 0)
    forks = data.get("total_forks", 0)
    pull_requests = data.get("total_pull_requests", 0)
    issues = data.get("total_issues", 0)
    total_contributions = data.get("contribution_calendar", {}).get("total_contributions", 0)

    labels = ["Stars", "Forks", "Pull Requests", "Issues", "Contributions"]
    values = [stars, forks, pull_requests, issues, total_contributions]

    # Calculate percentages
    total_sum = sum(values)
    if total_sum == 0:
        print("[WARNING] All metrics are zero — chart will be blank.")
        return

    percentages = [(v / total_sum) * 100 for v in values]

    # Fixed shape: use same value for all radar axes
    fixed_value = max(percentages)  # or set to a constant like 50
    fixed_percentages = [fixed_value] * len(values)

    # Close loops
    percentages += percentages[:1]
    fixed_percentages += fixed_percentages[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)

    # Create radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Plot actual percentages
    ax.plot(angles, percentages, linewidth=2, linestyle='solid', label="Activity %", color="blue")
    ax.fill(angles, percentages, alpha=0.25, color="skyblue")
    
    # Plot fixed polygon outline
    ax.plot(angles, fixed_percentages, linewidth=1, linestyle='dashed', color="gray", alpha=0.6)

    # Labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=14)
    ax.set_title(f"{username} - GitHub Activity Radar (Percentages)", size=20, weight='bold', pad=20)

    # Add percentage labels at equal distance from center
    fixed_radius = 50  # constant for all labels
    for i, (angle, pct, val) in enumerate(zip(angles, percentages, values + values[:1])):
        if i < len(labels):
            ax.text(
                angle,
                fixed_radius,
                f"{pct:.1f}% ({val})",
                ha='center',
                va='center',
                fontsize=18,
                fontweight='light',
                color="black"
            )

    ax.set_ylim(0, 100)
    ax.set_yticklabels([])

    # Save chart
    output_path = os.path.join(output_dir, f"{username}_radar_chart_percentages.png")
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[INFO] Radar chart saved to {output_path}")

if __name__ == "__main__":
    generate_radar_chart_with_percentages("IshaanPathak25")
