# charts/monthly_contribution_line.py
import os
import json
import matplotlib.pyplot as plt

def generate_monthly_chart(username):
    # Paths
    filepath = f"Github/data/{username}.json"
    output_dir = "Github/output/Graphics"
    os.makedirs(output_dir, exist_ok=True)

    # Load user data
    with open(filepath, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    monthly_contributions = user_data.get("monthly_contributions", {})

    if not monthly_contributions:
        # Create placeholder chart
        plt.figure(figsize=(9, 5))
        plt.text(0.5, 0.5, "No Monthly Contribution Data",
                 ha='center', va='center', fontsize=14)
        plt.axis("off")
        chart_path = os.path.join(output_dir, f"{username}_monthly_contribution_line.png")
        plt.savefig(chart_path, bbox_inches="tight", dpi=200)
        plt.close()
        print(f"⚠️ No monthly data found. Blank chart saved to {chart_path}")
        return

    # Prepare data
    months = list(monthly_contributions.keys())
    counts = list(monthly_contributions.values())

    # Plot
    plt.figure(figsize=(9, 6))
    plt.plot(months, counts, marker='o', linestyle='-', color='#4C72B0', linewidth=2)
    plt.fill_between(months, counts, color='#4C72B0', alpha=0.2)

    # Style
    plt.title(f"{username}'s Monthly Contributions", fontsize=14, fontweight='bold')
    plt.xlabel("Month", fontsize=12, fontweight='bold')
    plt.ylabel("Commits", fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().set_facecolor("#f9f9f9")

    # Save
    plt.tight_layout()
    chart_path = os.path.join(output_dir, f"{username}_monthly_contribution_line.png")
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    print(f"✅ Monthly contribution line chart saved to {chart_path}")