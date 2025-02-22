import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json

from Syllabot.data.Database import Database

# Set up the Flask app and specify the templates folder
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')

db = Database()  # instantiate your database

# Your API key and endpoint for the outline summary.
API_KEY = "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"
url = "https://openrouter.ai/api/v1/chat/completions"

# Your syllabus info (or any long text content)


@app.route("/", methods=["GET"])
def index():
    return render_template("projPage.html")

@app.route("/submit", methods=["POST"])
def submit():
    print("submit route reached", flush=True)

    # Get email and selected courses
    email = request.form.get("email")
    selected_courses = request.form.get("selected_courses")  # Example: "1,2,3"
    print("Selected courses received:", selected_courses, flush=True)

    if not email:
        flash("Email is required!")
        return redirect(url_for("index"))

    if not selected_courses:
        flash("No courses selected!")
        return redirect(url_for("index"))

    # Overwrite the previous registration for this email
    try:
        db.register_email_to_course(email, selected_courses)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("index"))

    # Convert course_id string ("1,2,3") into a list of integers
    try:
        course_id_list = [int(code.strip()) for code in selected_courses.split(",") if code.strip()]
    except ValueError:
        flash("Invalid course ID format!")
        return redirect(url_for("index"))

    # Fetch course outlines from the database
    course_outlines = db.fetch_course_outlines(course_id_list)
    print("Fetched Course Outlines:", course_outlines, flush=True)

    # Ensure we have valid outlines before proceeding
    if not course_outlines:
        session['summary'] = "Error: No valid course outlines found."
        flash("No valid course outlines found!")
        return redirect(url_for("result"))

    # Combine all outlines into one text for summarization
    outline_text = "\n\n".join(course_outlines)
    print("Outline Text for API:", outline_text, flush=True)

    # Prepare API call for syllabus summary
    prompt = f"Summarize the following course outlines in a structured format add bold headers for eaech heading aswell as bullet points:\n\n{outline_text}"

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Make the API call and handle errors
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

     # 🔍 Debugging: Print full API response
        print("Raw API Response:", json.dumps(response_json, indent=2), flush=True)

    # Check if API returned choices
        if "choices" in response_json and isinstance(response_json["choices"], list) and response_json["choices"]:
         summary = response_json["choices"][0]["message"]["content"]
        else:
            print("Error: Unexpected API response format", flush=True)
            summary = f"Error: No valid response received. API response: {response_json}"

    except requests.exceptions.RequestException as e:
        print("API Request Failed:", str(e), flush=True)
        summary = "Error: Failed to connect to API."

    # Store summary and redirect
    session['summary'] = summary
    flash("Registration successful!")
    return redirect(url_for("result"))



@app.route("/result", methods=["GET"])
def result():
    summary = session.get("summary", "No summary available.")
    return render_template("result.html", output=summary)

if __name__ == "__main__":
    app.run(debug=True)