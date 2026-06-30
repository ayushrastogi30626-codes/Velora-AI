import streamlit as st
from backend.chatbot import stream_ai_response
from backend.pdf_reader import extract_text_from_pdf
from backend.pdf_vector import PDFVectorStore
from backend.pdf_chunker import split_text
from backend.agent import run_agent
def llm_call(prompt):
    response = ""

    for chunk in stream_ai_response([
        {"role": "user", "content": prompt}
    ]):
        response += chunk

    return response

# -----------------------------
# INIT STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "vector_store" not in st.session_state:
    st.session_state.vector_store = PDFVectorStore()

# -----------------------------
# UI TITLE
# -----------------------------
st.title("🤖 My AI Assistant")

# -----------------------------
# PDF UPLOAD SECTION
# -----------------------------
uploaded_pdf = st.file_uploader("📄 Upload PDF", type=["pdf"])

if uploaded_pdf is not None:
    text = extract_text_from_pdf(uploaded_pdf)

    chunks = split_text(text)

    st.session_state.vector_store.build_index(chunks)

    st.session_state.pdf_text = text

    st.success("PDF is now AI searchable 🔥")
    pdf_question = st.text_input("Ask something from PDF")
    if pdf_question:
      answer = run_agent(
        pdf_question,
        st.session_state.vector_store,
        llm_call
    )

    with st.chat_message("assistant"):
        st.write(answer)

# -----------------------------
# SUMMARIZE BUTTON
# -----------------------------
if st.button("🧠 Summarize PDF"):

    if st.session_state.pdf_text == "":
        st.warning("Please upload a PDF first")

    else:
        prompt = f"""
Summarize this document in simple bullet points:

{st.session_state.pdf_text[:3000]}
"""

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            for chunk in stream_ai_response([
                {"role": "user", "content": prompt}
            ]):
                full_response += chunk
                placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

# -----------------------------
# CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
prompt = st.chat_input("Type your message here...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        messages = st.session_state.messages[-10:]

        for chunk in stream_ai_response(messages, st.session_state.pdf_text):
            full_response += chunk
            placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

    # AI response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # IMPORTANT: only last 10 messages (memory optimization)
        messages = st.session_state.messages[-10:]

        for chunk in stream_ai_response(messages, st.session_state.pdf_text):
            full_response += chunk
            placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
    #LLM WRAPPER
    def llm_call(prompt):
        response = ""
        for chunk in stream_ai_response([
            {"role":"user","content": prompt}
        ]):
            response += chunk
        return response