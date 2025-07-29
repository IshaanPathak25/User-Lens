from flask import Flask, render_template, request, redirect, url_for
import os
from Reddit.main import run_reddit_pipeline
from Github.main import run_github_pipeline
from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

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
            result_path = f"Reddit/output/Script/{username}_reddit_profile.txt"
            
        elif platform == "github":
            username = url.strip().split("/")[-1]  # e.g., https://github.com/USERNAME
            run_github_pipeline(username)
            result_path = f"Github/output/{username}_github_profile.txt"
            
        else:
            return "❌ Invalid platform selected."

        # output_path = f"{platform.capitalize()}/output/Script/{username}_{platform.lower()}_profile.txt"
        with open(result_path, "r", encoding='utf-8') as f:
            result_text = f.read()

        return render_template("result.html", result=result_text)

    except Exception as e:
        return f"❌ {platform.capitalize()} Analysis Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)