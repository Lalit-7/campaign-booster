from flask import Flask, render_template, request, jsonify
import re
import os
import requests
import google.generativeai as genai


# ---- load .env if present ----
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = Flask(__name__)

# ---- API KEY ----
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("KEY LOADED:", bool(GEMINI_API_KEY))

genai.configure(api_key=GEMINI_API_KEY)

# ------------------------------
# BASIC RULE-BASED SCORING LOGIC
# ------------------------------
def score_campaign(title, description, goal):
    score = 0
    suggestions = []

    words = len(description.split())

    # Length
    if words < 120:
        suggestions.append("Add more details about the situation and background.")
    elif words > 600:
        suggestions.append("Try to keep the story focused and easier to read.")
    else:
        score += 15

    # Use of funds
    if re.search(r"\d", description):
        score += 10
    else:
        suggestions.append("Mention exact expenses (bills, medicines, surgery cost, etc.)")

    # Proof
    if any(x in description.lower() for x in ["bill", "document", "report"]):
        score += 10
    else:
        suggestions.append("Add hospital bills/reports for transparency.")

    # Urgency
    if any(x in description.lower() for x in ["urgent", "critical", "immediately", "emergency"]):
        score += 10

    # CTA
    if "share" in description.lower() or "support" in description.lower():
        score += 10
    else:
        suggestions.append("Ask people clearly to donate and share the campaign.")

    # Breakdown clarity
    if "will be used" in description.lower() or "utilized" in description.lower():
        score += 15
    else:
        suggestions.append("Explain clearly how every rupee will be used.")

    # Readability
    if words / max(description.count("."), 1) < 25:
        score += 10

    # Photos / updates
    if any(x in description.lower() for x in ["photo", "image", "update"]):
        score += 10
    else:
        suggestions.append("Post regular updates and real photos to build trust.")

    # Goal
    try:
        if float(goal) > 0:
            score += 10
    except:
        pass

    trust_level = "High" if score >= 70 else "Medium" if score >= 45 else "Low"
    return score, trust_level, suggestions


# ------------------------------
# GEMINI AI REWRITE
# ------------------------------
def gemini_rewrite(title, description):
    if not GEMINI_API_KEY:
        return title, description

    prompt = f"""
Rewrite the fundraiser content clearly, emotionally and honestly.

Return ONLY this format:

Title: <better title>
Story: <rewritten story>

Title: {title}
Story: {description}
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)

        text = response.text or ""

        better_title = title
        better_story = description

        for line in text.split("\n"):
            if line.lower().startswith("title"):
                better_title = line.split(":",1)[1].strip()
            if line.lower().startswith("story"):
                better_story = text[text.lower().find("story:")+6:].strip()
                break

        return better_title, better_story

    except Exception as e:
        print("GEMINI ERROR:", e)
        return title, description


# ------------------------------
# ROUTES
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    title = data.get("title", "")
    description = data.get("description", "")
    goal = data.get("goal", "0")

    score, trust_level, suggestions = score_campaign(title, description, goal)
    better_title, better_story = gemini_rewrite(title, description)

    return jsonify({
        "score": score,
        "trust_level": trust_level,
        "suggestions": suggestions,
        "better_title": better_title,
        "better_story": better_story
    })


if __name__ == "__main__":
    app.run(debug=True)
