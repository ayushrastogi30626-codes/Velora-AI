import streamlit as st


from backend.chatbot import stream_ai_response
from backend.pdf_reader import extract_text_from_pdf
from backend.pdf_vector import PDFVectorStore
from backend.pdf_chunker import split_text
from backend.agent import run_agent


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="🤖 Velora AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------
# CUSTOM COLORS
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:#0E1117;
}

h1,h2,h3{
    color:white;
}

[data-testid="stSidebar"]{
    background:#161B22;
}

div.stButton > button{
    background:#4F46E5;
    color:white;
    border-radius:10px;
    border:none;
    height:45px;
}

div.stButton > button:hover{
    background:#6366F1;
}

.stChatMessage{
    border-radius:12px;
    padding:12px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# LLM WRAPPER
# ---------------------------------------------------

def llm_call(prompt):

    response = ""

    for chunk in stream_ai_response(
        [
            {
                "role":"user",
                "content":prompt
            }
        ]
    ):
        response += chunk

    return response


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text=""

if "vector_store" not in st.session_state:
    st.session_state.vector_store=PDFVectorStore()



# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🤖 Velora AI")

st.caption("🚀 AI Assistant powered by Gemini")


st.divider()


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("⚙️ Velora")

    st.success("AI Assistant Ready")

    uploaded_pdf=st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

    summarize=st.button("🧠 Summarize PDF")

   
# PDF PROCESSING
# ---------------------------------------------------

if uploaded_pdf is not None:

    with st.spinner("📄 Reading PDF..."):

        text = extract_text_from_pdf(uploaded_pdf)

        chunks = split_text(text)

        st.session_state.vector_store.build_index(chunks)

        st.session_state.pdf_text = text

    st.success("✅ PDF uploaded and indexed successfully!")

    st.info(f"📄 Total Characters: {len(text)}")
    st.info(f"🧩 Total Chunks: {len(chunks)}")

    pdf_question = st.text_input(
        "💬 Ask anything about your PDF",
        placeholder="Example: Summarize chapter 2"
    )

    if pdf_question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": pdf_question
            }
        )

        with st.chat_message("assistant"):

            with st.spinner("🤖 Searching PDF..."):

                answer = run_agent(
                    pdf_question,
                    st.session_state.vector_store,
                    llm_call
                )

        st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

# ---------------------------------------------------
# PDF SUMMARY
# ---------------------------------------------------

if summarize:

    if st.session_state.pdf_text == "":

        st.warning("⚠️ Please upload a PDF first.")

    else:

        prompt = f"""
Summarize the following PDF in simple bullet points.

PDF Content:

{st.session_state.pdf_text}
"""

        with st.chat_message("assistant"):

            with st.spinner("🧠 Generating Summary..."):

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
        # ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

st.divider()

st.subheader("💬 AI Chat")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

prompt = st.chat_input("💬 Ask Velora AI anything...")

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

        with st.spinner("🤖 Velora AI is thinking..."):

            placeholder = st.empty()

            full_response = ""

            messages = st.session_state.messages[-10:]

            for chunk in stream_ai_response(messages):

                full_response += chunk
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )



# ---------------------------------------------------

# SIDEBAR UTILITIES
# ---------------------------------------------------

with st.sidebar:

    st.divider()

    st.subheader("🛠 Utilities")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.success("Chat history cleared!")

        st.rerun()

    st.divider()

    st.markdown("### 📊 Statistics")

    st.write(f"💬 Messages: {len(st.session_state.messages)}")

    if st.session_state.pdf_text != "":
        st.success("📄 PDF Loaded")
    else:
        st.info("📄 No PDF Uploaded")
