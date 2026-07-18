from ollama import chat

response = chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "Say Hello"
        }
    ]
)

print(response["message"]["content"])