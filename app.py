
import streamlit as st

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

from backend.chatbot import stream_ai_response
from backend.pdf_reader import extract_text_from_pdf
from backend.pdf_vector import PDFVectorStore
from backend.pdf_chunker import split_text
from backend.agent import run_agent

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
import streamlit as st
from backend.chatbot import stream_ai_response
from backend.pdf_reader import extract_text_from_pdf
from backend.pdf_vector import PDFVectorStore
from backend.pdf_chunker import split_text
from backend.agent import run_agent


# -----------------------------
# LLM WRAPPER
# -----------------------------
def llm_call(prompt):
    response = ""

    for chunk in stream_ai_response([
        {"role": "user", "content": prompt}
    ]):
        response += chunk

    return response


# -----------------------------
# INIT SESSION STATE
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
st.title("🤖 Velora AI")


# -----------------------------
# PDF UPLOAD
# -----------------------------
with st.sidebar:
    st.header("📄 PDF Tools")

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    summarize = st.button("🧠 Summarize PDF")


if uploaded_pdf is not None:

    text = extract_text_from_pdf(uploaded_pdf)

    chunks = split_text(text)

    st.session_state.vector_store.build_index(chunks)
    st.write("Text length:", len(text))
    st.write("Chunks:", len(chunks))
    st.write("Vector Index:", st.session_state.vector_store.index)

    st.session_state.pdf_text = text

    st.success("✅ PDF is now AI searchable!")

    pdf_question = st.text_input(
        "Ask something from the PDF"
    )

    if pdf_question:

        # Save user question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": pdf_question
            }
        ) 

        answer = run_agent(
            pdf_question,
            st.session_state.vector_store,
            llm_call
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save assistant reply
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# -----------------------------
# SUMMARIZE PDF
# -----------------------------
# -----------------------------
# SUMMARIZE PDF
# -----------------------------
if st.button("🧠 Summarize PDF"):

    if st.session_state.pdf_text == "":
        st.warning("Please upload a PDF first.")

    else:

        prompt = f"""
Please summarize the following PDF in simple bullet points.

PDF Content:
{st.session_state.pdf_text}
"""

        with st.chat_message("assistant"):

            placeholder = st.empty()
            full_response = ""

            for chunk in stream_ai_response([
                {
                    "role": "user",
                    "content": prompt
                }
            ]):

                full_response += chunk
                placeholder.markdown(full_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
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
prompt = st.chat_input(
    "Type your message here..."
)

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        # Only keep last 10 messages
        messages = st.session_state.messages[-10:]

        for chunk in stream_ai_response(messages):
     

            full_response += chunk
            placeholder.markdown(full_response)

    # Save assistant reply
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )