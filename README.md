# 🤖 Velora AI

An intelligent AI-powered assistant built with **Python**, **Streamlit**, and **Google Gemini**.

Velora AI allows users to chat with an AI assistant, upload PDF documents, generate AI-powered summaries, and ask questions about uploaded PDFs using semantic search.

---

## ✨ Features

- 💬 AI-powered conversational assistant
- 📄 Upload and analyze PDF documents
- 🧠 Generate concise PDF summaries
- ❓ Ask questions from uploaded PDFs
- 🔍 Semantic search using FAISS and Sentence Transformers
- 🎨 Clean and modern Streamlit interface

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | User Interface |
| FAISS | Vector Database |
| Sentence Transformers | Text Embeddings |
| PyPDF | PDF Text Extraction |
| NumPy | Numerical Operations |

---

## 📂 Project Structure

```text
Velora-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── backend/
    |---agent.py
│   ├── chatbot.py
│   ├── agent.py
│   ├── pdf_chunker.py
│   ├── pdf_reader.py
│   ├── pdf_vector.py
│   └── tools.py
│

```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ayushrastogi30626-codes/Velora-AI.git
```

### 2. Move into the project

```bash
cd Velora-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📖 How to Use

1. Launch Velora AI.
2. Upload a PDF document.
3. Click **Summarize PDF** to generate an AI summary.
4. Ask questions related to the uploaded PDF.
5. Chat naturally with the AI assistant.

---

## 📸 Screenshots

Add screenshots of your application here.

Example:

- Home Screen
- PDF Upload
- PDF Summary
- Chat Interface

---

## 🎯 Future Enhancements

- 🎙️ Voice Assistant
- 🌍 Multi-language Support
- 📝 Chat History Export
- 📑 Support for Multiple PDFs
- 📷 OCR for Scanned PDFs
- 🌐 Web Search Integration
- 📊 Better UI & Analytics
     

---

## 👨‍💻 Author

**Ayush Rastogi**

GitHub: https://github.com/ayushrastogi30626-codes

---

## 📄 License

This project is licensed under the MIT License.