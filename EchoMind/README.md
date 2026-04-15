# 🧠 EchoMind - AI Memory-Powered Chat System

EchoMind is an advanced conversational AI system that combines **LLMs (Groq/OpenAI)** with **persistent vector memory (ChromaDB)** to create intelligent, context-aware conversations.

It goes beyond traditional chatbots by **remembering past interactions**, enabling more natural, personalized, and continuous dialogue.

---

## 🚀 Features

- 💬 Context-aware chat with memory
- 🧠 Persistent long-term memory using ChromaDB
- ⚡ Fast LLM inference via Groq / OpenAI
- 🌐 Multiple interfaces (CLI, Web UI, API)
- 🔌 Modular and scalable architecture
- 🧪 Unit testing for all core components

---

## 🏗️ Architecture Overview

EchoMind follows a modular pipeline:

1. **User Input**
2. **Prompt Engineering**
3. **Memory Retrieval (ChromaDB)**
4. **LLM Processing (Groq/OpenAI)**
5. **Response Generation**
6. **Memory Storage**

---

## 📂 Project Structure
```
EchoMind/
│
├── data/
│ ├── raw/ # Original chat logs
│ ├── processed/ # Cleaned conversations
│ └── external/ # External datasets
│
├── notebooks/
│ ├── 01_exploration.ipynb # Test APIs and models
│ ├── 02_memory_test.ipynb # Test ChromaDB memory
│ └── 03_final_demo.ipynb # Final demo notebook
│
├── src/
│ ├── init.py
│ ├── model.py # LLM connection (Groq/OpenAI)
│ ├── memory.py # ChromaDB vector memory
│ ├── pipeline.py # Chat pipeline
│ ├── prompt.py # Prompt templates
│ └── utils.py # Helper functions
│
├── models/
│ ├── saved/ # Saved embeddings
│ └── checkpoints/ # Memory snapshots
│
├── app/
│ ├── main.py # CLI entry point
│ ├── streamlit_app.py # Web UI
│ ├── api.py # FastAPI backend
│ ├── routes/
│ │ ├── chat.py # /chat endpoint
│ │ └── memory.py # /memory endpoint
│ └── static/
│ ├── style.css
│ └── logo.png
│
├── tests/
│ ├── test_model.py
│ ├── test_memory.py
│ └── test_pipeline.py
│
├── reports/
│ ├── figures/
│ └── final_report.md
│
├── docs/
│ ├── architecture.md
│ ├── api_docs.md
│ └── demo.md
│
├── .env # API keys (DO NOT COMMIT)
├── .gitignore
├── README.md
├── requirements.txt
└── config.yaml
```

---

## ⚙️ Installation

```bash
git clone https://github.com/XC0ID/AI-Trinity.git
cd AI-Trinity/EchoMind
pip install -r requirements.txt
```

---

##🔌 API Endpoints
```
/chat
```
* Handles conversation requests
* Returns AI-generated responses with memory context
```
/memory
```
* Stores and retrieves conversation embeddings
* Enables long-term memory functionality

---
## 📊 Notebooks
01_exploration.ipynb → Experiment with models and APIs
02_memory_test.ipynb → Validate memory storage and retrieval
03_final_demo.ipynb → End-to-end demonstration
📈 Future Improvements
Add multi-user session memory
Improve semantic search accuracy
Integrate voice-based interaction
Deploy on cloud (AWS/GCP)

---
## 🤝 Contributing

Contributions are welcome!

Fork the repository
Create a new branch
Make your changes
Submit a pull request

---
## 📜 License

This project is licensed under the MIT License.
