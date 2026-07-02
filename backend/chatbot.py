import ollama
import re

# -------------------------
# SYSTEM PROMPT
# -------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are a helpful AI assistant.

Rules:
- Answer clearly.
- Keep responses concise unless more detail is requested.
- If the user starts with 'calculate', solve the expression.
"""
}

# -------------------------
# CALCULATOR
# -------------------------
def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"


# -------------------------
# AI RESPONSE
# -------------------------
def stream_ai_response(messages):

    last_message = messages[-1]["content"].lower()

    # Calculator
    if last_message.startswith("calculate"):
        expression = last_message.replace("calculate", "").strip()
        yield f"🧮 Result: {calculator_tool(expression)}"
        return

    # Normal AI Chat
    messages = [SYSTEM_PROMPT] + messages

    stream = ollama.chat(
        model="phi3",
        messages=messages,
        stream=True
    )

    for chunk in stream:
        yield chunk["message"]["content"]