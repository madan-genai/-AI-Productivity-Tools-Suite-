# 🚀 AI Productivity Tools Suite

An AI-powered productivity platform built using LangGraph, LangChain, FastAPI, and Streamlit. The suite combines multiple AI utilities into a single application to help users summarize content, improve writing quality, translate text, and generate image descriptions.

---

## 📌 Features

### 📝 AI Text Summarizer
- Summarizes long-form text into concise summaries
- Supports different summary lengths
- Preserves key information and context

### ✅ AI Grammar Checker
- Detects grammar, spelling, and punctuation errors
- Generates corrected text
- Improves readability and sentence structure

### 🌍 AI Translator
- Translates text into multiple languages
- Maintains contextual meaning
- Fast and accurate language conversion

### 🖼️ AI Image Describer
- Generates descriptions from uploaded images
- Supports multimodal AI workflows
- Useful for accessibility and content understanding

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
LangGraph Workflow
 ├── Summarization Node
 ├── Grammar Checker Node
 ├── Translation Node
 └── Image Description Node
 │
 ▼
LLM / Vision Model
 │
 ▼
Response
```

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- LangGraph
- LangChain
- Pydantic

### Frontend
- Streamlit

### AI Models
- Google Gemini
- Hugging Face Models

### Utilities
- Pillow
- Requests
- Python-dotenv

---

## 📂 Project Structure

```text
AI-Productivity-Tools-Suite/
│
├── backend/
│   ├── main.py
│   ├── graph.py
│   ├── models.py
│   └── nodes/
│
├── frontend/
│   └── streamlit_app.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Productivity-Tools-Suite.git
cd AI-Productivity-Tools-Suite
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_api_key
```

---

## ▶️ Run Backend

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

---

## ▶️ Run Frontend

```bash
streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## 📡 API Endpoints

### Text Summarization

```http
POST /summarize
```

### Grammar Checking

```http
POST /grammar-check
```

### Translation

```http
POST /translate
```

### Image Description

```http
POST /image-description
```

---

## 🔄 LangGraph Workflow

```text
Input
 │
 ▼
Task Selection
 │
 ├── Summarization
 ├── Grammar Correction
 ├── Translation
 └── Image Description
 │
 ▼
LLM Processing
 │
 ▼
Output
```

---

## 🚀 Future Enhancements

- RAG-based document chat
- Voice-to-text support
- Text-to-speech responses
- Multi-agent workflows
- User authentication
- Conversation memory
- PDF and DOCX support

---

## 👨‍💻 Author

Madan Lal

AI Engineer | Agentic AI Developer

Portfolio:
https://portfolio-website-three-omega.vercel.app/

---

## 📜 License

This project is licensed under the MIT License.
