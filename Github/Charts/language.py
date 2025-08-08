import json
import os
import matplotlib.pyplot as plt
import numpy as np

def generate_language_pie_chart(username):
    data_path = f"Github/data/{username}.json"
    output_dir = "Github/output/Graphics"
    os.makedirs(output_dir, exist_ok=True)

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    language_totals = {}
    for repo in data.get("repos", []):
        for lang, bytes_of_code in repo.get("all_languages", {}).items():
            language_totals[lang] = language_totals.get(lang, 0) + bytes_of_code

    if not language_totals:
        print("⚠️ No language data found.")
        return

    sorted_langs = dict(sorted(language_totals.items(), key=lambda item: item[1], reverse=True))
    labels = list(sorted_langs.keys())
    sizes = list(sorted_langs.values())

    total = sum(sizes)
    explode = [0.1 if (100 * size / total) < 5 else 0 for size in sizes]

    fig, ax = plt.subplots(figsize=(9, 9))
    wedges, _ = ax.pie(
        sizes,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=1, edgecolor='white'),
        explode=explode
    )

    # Variables for staggered label offsets
    small_threshold = 5  # percent
    offset_gap = 0.12
    last_angle_side = None
    small_counter = 0

    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        percentage = 100. * sizes[i] / total

        # Determine which side of pie (left or right)
        side = "right" if x >= 0 else "left"

        # If small slice, stagger label positions
        if percentage < small_threshold:
            if side == last_angle_side:
                small_counter += 1
            else:
                small_counter = 0
            last_angle_side = side

            # Offset position vertically for staggered effect
            y_offset = y + (offset_gap * small_counter if side == "right" else -offset_gap * small_counter)

            ax.annotate(
                f"{labels[i]} ({percentage:.1f}%)",
                xy=(x, y), xytext=(1.2 * np.sign(x), y_offset),
                ha='left' if side == "right" else 'right',
                va='center',
                fontsize=10,
                fontweight='bold',
                arrowprops=dict(arrowstyle='-', color='black', lw=0.8, connectionstyle="arc3,rad=0.0")
            )
        else:
            # Large slice label inside
            ax.text(
                0.6 * x,
                0.6 * y,
                f"{percentage:.1f}%",
                ha='center',
                va='center',
                fontsize=12,
                fontweight='bold'
            )

    ax.axis("equal")
    plt.title(f"{username}'s Language Usage", fontsize=14)

    ax.legend(
        wedges,
        labels,
        title="Languages",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=10
    )

    plt.tight_layout()
    chart_path = os.path.join(output_dir, f"{username}_language_chart.png")
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    print(f"✅ Language pie chart saved to {chart_path}")

# if __name__ == "__main__":
#     generate_language_pie_chart("YOUR_GITHUB_USERNAME")