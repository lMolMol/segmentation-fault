import requests

API_KEY = "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"
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("bruh")
token = 0

while token < 9:
    inp = input("Enter your input: ")
    token+=1

    data = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",  # or another available model like "mixtral"
        "messages": [{"role": "user", "content": f"{inp}"}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # Extract the content only
    content = response_json["choices"][0]["message"]["content"]
    print(content)

"""import google.generativeai as genai

client = genai.Client(api_key="YOUR_API_KEY")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)"""