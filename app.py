from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask import send_file
from Reddit.main import run_reddit_pipeline
from Github.main import run_github_pipeline
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def home():
    return render_template("index.html")


# Analyze user profile
@app.route("/analyze", methods=["POST"])
def analyze():
    platform = request.form.get("platform")
    url = request.form.get("url")

    if not platform or not url:
        flash("❌ Please select a platform and enter a profile URL.")
        return redirect(url_for("home"))

    try:
        # Safely extract username
        if platform == "reddit":
            if "/user/" not in url:
                flash("❌ Invalid Reddit URL format.")
                return redirect(url_for("home"))
            username = url.strip().split("/user/")[-1].strip("/")

            run_reddit_pipeline(username)
            result_path = f"Reddit/output/Script/{username}_reddit_profile.txt"

        elif platform == "github":
            if "github.com/" not in url:
                flash("❌ Invalid GitHub URL format.")
                return redirect(url_for("home"))
            username = url.strip().split("github.com/")[-1].strip("/")

            run_github_pipeline(username)
            result_path = f"Github/output/{username}_github_profile.txt"

        else:
            flash("❌ Invalid platform selected.")
            return redirect(url_for("home"))

        # Check result file exists
        if not os.path.exists(result_path):
            flash(f"❌ Could not generate profile for {username}. Please check the username or try again.")
            return redirect(url_for("home"))

        # Load and pass result
        with open(result_path, "r", encoding="utf-8") as f:
            result_text = f.read()

        return render_template("result.html", result=result_text, username=username, platform=platform.capitalize())

    except Exception as e:
        print("❌ ERROR:", e)  # Debug log
        flash(f"❌ {platform.capitalize()} Analysis Error: {str(e)}")
        return redirect(url_for("home"))
    
# Download persona image

@app.route("/download_persona", methods=["POST"])
def download_persona():
    platform = request.form.get("platform")
    username = request.form.get("username")

    try:
        if platform == "Reddit":
            from Reddit.visual_generator import generate_visual_persona
            generate_visual_persona(username)
            filepath = f"Reddit/output/Image/{username}_reddit_persona.png"
        elif platform == "GitHub":
            from Github.visual_generator import generate_visual_persona
            generate_visual_persona(username)
            filepath = f"Github/output/Image/{username}_github_persona.png"
        else:
            flash("❌ Invalid platform selected.")
            return redirect(url_for("home"))

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        flash(f"❌ Failed to generate or download persona image: {e}")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
    