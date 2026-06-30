import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Hello! My name is Ayush. Tell me a fun fact."
        }
    ]
)

print(response["message"]["content"])
import ollama

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("AI:", response["message"]["content"])