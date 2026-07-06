import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


# -------------------------
# SYSTEM PROMPT
# -------------------------
SYSTEM_PROMPT = """
You are a helpful AI assistant.

Rules:
- Answer clearly.
- Keep responses concise unless more detail is requested.
- If the user starts with 'calculate', solve the expression.
"""


# -------------------------
# Calculator
# -------------------------
def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"


# -------------------------
# AI RESPONSE
# -------------------------
# -------------------------
# AI RESPONSE
# -------------------------
from google.api_core.exceptions import ResourceExhausted


def stream_ai_response(messages):

    last_message = messages[-1]["content"].lower()

    # Calculator
    if last_message.startswith("calculate"):
        expression = last_message.replace("calculate", "").strip()
        yield f"🧮 Result: {calculator_tool(expression)}"
        return

    # Build conversation
    conversation = SYSTEM_PROMPT + "\n\nConversation:\n"

    for msg in messages:
        conversation += f"{msg['role'].capitalize()}: {msg['content']}\n"

    conversation += "\nAssistant:"

    try:
        # Generate AI response
        response = model.generate_content(conversation)

        if response.text:
            yield response.text
        else:
            yield "⚠️ No response was generated. Please try again."

    except ResourceExhausted:
        yield """
# ⚠️ AI Usage Limit Reached

Sorry! Velora AI has reached its current free usage limit.

### Please try one of the following:
- ⏳ Wait a few minutes and try again.
- 🌅 If the daily quota has been exhausted, please come back tomorrow.

Thank you for using **Velora AI** ❤️
"""

    except Exception:
        yield """
# ⚠️ Something Went Wrong

Velora AI couldn't process your request right now.

Please try again in a few moments.
"""