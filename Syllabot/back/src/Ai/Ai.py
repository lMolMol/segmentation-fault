from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Your API key and endpoint
API_KEY = ""
url = "https://openrouter.ai/api/v1/chat/completions"

# Your syllabus info (or any long text content)
info = """ """

def byWeek(week, outLine):
    inp = f"Summarize the following content and extract only info from week {week} according to important dates (NO PARAGRAPH FORMAT) [ADD IMPORTANT DETAILS ONLY]: " + outLine

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [{"role": "user", "content": inp}],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if "choices" in response_json:
        content = response_json["choices"][0]["message"]["content"]
    else:
        content = "Error: No valid response received."

    return content

"""
//
//
//

"""

def summarize(courseOutline):
    inp = "Summarize the following content into clean lines and spacings between each one according to important dates (NO PARAGRAPH FORMAT) [ADD IMPORTANT DETAILS ONLY]: " + courseOutline

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [{"role": "user", "content": inp}],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if "choices" in response_json:
        content = response_json["choices"][0]["message"]["content"]
    else:
        content = "Error: No valid response received."

    return content

@app.route("/", methods=["GET"])
def index():
    # Render the main HTML page (index.html)
    return render_template("projPage.html")

@app.route("/submit", methods=["POST"])
def submit():
    # In a more complex example you could extract form data here (email, course selections, etc.)
    # For now, we use a fixed prompt that combines instructions with your syllabus info.
    inp = "Summarize the following content into clean lines and spacings between each one (NO PARAGRAPH FORMAT) [ADD IMPORTANT DETAILS ONLY]: " + info

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [{"role": "user", "content": inp}],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if "choices" in response_json:
        content = response_json["choices"][0]["message"]["content"]
    else:
        content = "Error: No valid response received."

    # Pass the output to the result page template
    return render_template("result.html", output=content)


if __name__ == "__main__":
    app.run(debug=True)
