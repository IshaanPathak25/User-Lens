from flask import Flask, render_template, request, redirect, url_for
import os
from Reddit.main import run_reddit_pipeline
from Github.main import run_github_pipeline

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    platform = request.form.get("platform")
    url = request.form.get("url")

    if not platform or not url:
        return redirect(url_for("home"))

    try:
        if platform == "reddit":
            username = url.strip().split("/")[-2]  # e.g., https://www.reddit.com/user/USERNAME/
            run_reddit_pipeline(username)
        elif platform == "github":
            username = url.strip().split("/")[-1]  # e.g., https://github.com/USERNAME
            run_github_pipeline(username)
        else:
            return "❌ Invalid platform selected."

        return render_template("result.html", platform=platform.capitalize(), username=username)

    except Exception as e:
        return f"❌ {platform.capitalize()} Analysis Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
