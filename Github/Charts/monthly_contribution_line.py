import os
import json
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_monthly_chart(username):
    """
    Generates an HTML file showing monthly contributions with:
      - Initial view = last 8 months (if available)
      - Rangeslider always showing the full timeline
      - Scrollable/pannable chart with Y-axis auto-scaling
    """
    # Paths
    filepath = f"Github/data/{username}.json"
    output_dir = "Github/output/Graphics"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{username}_monthly_contribution_chart.html")

    # Load JSON
    with open(filepath, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    monthly_contributions = user_data.get("monthly_contributions", {})
    if not monthly_contributions:
        return None

    # Ensure chronological order
    items = sorted(monthly_contributions.items(), key=lambda kv: kv[0])  # YYYY-MM sort works
    months = [datetime.strptime(k, "%Y-%m") for k, _ in items]
    counts = [v for _, v in items]

    # Create plot
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(
        x=months,
        y=counts,
        mode="lines+markers",
        fill="tozeroy",
        line=dict(color="#4C72B0", width=2),
        marker=dict(size=6)
    ))

    # Set rangeslider to full range
    fig.update_layout(
        title=f"{username}'s Monthly Contributions",
        xaxis_title="Month",
        yaxis_title="Commits",
        xaxis=dict(
            tickangle=45,
            rangeslider=dict(
                visible=True,
                range=[months[0], months[-1]]  # full dataset range
            ),
            type="date"
        ),
        yaxis=dict(autorange=True, fixedrange=False),
        template="plotly_white",
        height=800
    )

    # Initial zoom = last 8 months (or all if less than 8)
    if len(months) > 8:
        fig.update_xaxes(range=[months[-8], months[-1]])

    # Save HTML
    fig.write_html(output_path, include_plotlyjs="cdn")
    return output_path