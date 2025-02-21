from gpt4all import GPT4All

model_path = "models/mistral-7b-instruct.gguf"  # Example model
model = GPT4All(model_path)

# Generate a response
response = model.generate("said hi!!")
print(response)