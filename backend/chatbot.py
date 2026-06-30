import ollama
import re

# -------------------------
# SYSTEM BRAIN
# -------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are an AI Agent.

You can:
1. Answer normally
2. Use tools when needed

Rules:
- If math is asked → use calculator tool
- If PDF question → use context
- Otherwise answer normally
- Be short and clear
"""
}

# -------------------------
# TOOL 1: CALCULATOR
# -------------------------
def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

# -------------------------
# TOOL 2: PDF SEARCH (simple version)
# -------------------------
def search_pdf(question, pdf_text):
    if not pdf_text:
        return "No PDF uploaded"

    return pdf_text[:1500]  # simple version for now

# -------------------------
# AGENT CORE
# -------------------------
def stream_ai_response(messages, pdf_text=""):

    last_message = messages[-1]["content"].lower()

    # -------------------------
    # TOOL DECISION: CALCULATOR
    # -------------------------
    if "calculate" in last_message:
        expression = re.sub(r"calculate", "", last_message)
        result = calculator_tool(expression)
        yield f"🧮 Result: {result}"
        return

    # -------------------------
    # TOOL DECISION: PDF
    # -------------------------
    if "pdf" in last_message or "document" in last_message:
        result = search_pdf(last_message, pdf_text)
        yield f"📄 From PDF:\n{result}"
        return

    # -------------------------
    # NORMAL AI RESPONSE
    # -------------------------
    messages = [SYSTEM_PROMPT] + messages[-10:]

    stream = ollama.chat(
        model="phi3",
        messages=messages,
        stream=True,
        options={
            "temperature": 0.7,
            "top_p": 0.9
        }
    )

    for chunk in stream:
        yield chunk["message"]["content"]