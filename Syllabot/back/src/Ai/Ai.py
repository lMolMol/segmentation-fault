import requests

API_KEY = "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"
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

token = 0

while token < 9:
    token+=1
    inp = input("enter prompt: ")

    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",  # or another available model like "mixtral"
        "messages": [{"role": "user", "content": f"{inp}"}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # Extract the content only
    if not response_json["choices"]:
        print("no answer...")
    else:
        content = response_json["choices"][0]["message"]["content"]
        print(content)