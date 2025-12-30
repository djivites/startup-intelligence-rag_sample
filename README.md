

# 🚀 Startup Intelligence RAG System

**AI-Powered Funding & Startup Intelligence Platform**

---

## 📌 Overview

**Startup – Funder Intelligence Hub** is a **Retrieval-Augmented Generation (RAG)** based AI system designed to help founders, investors, and analysts discover reliable startup intelligence from real-world sources.

The platform automatically **collects, processes, understands, and retrieves startup-related information** from news articles, blogs, and reports, enabling users to ask natural-language questions and receive **fact-grounded, citation-backed insights**.

This system is built with **LangChain + Ollama + ChromaDB**,as of now ollama is implemented further we will be changing from ollama to gemini for better results, and supports **multilingual queries**, **context-aware reasoning**, and **structured information extraction**.

---


---

## 🎯 Key Objectives

* Reduce manual research time for startup and investment intelligence
* Provide verified, citation-backed answers using trusted data sources
* Enable intelligent **investor–startup matching** through contextual understanding
* Support **multilingual and cross-lingual queries** for wider accessibility
* Minimize hallucinations using a **grounded Retrieval-Augmented Generation (RAG)** architecture
* Enable **document upload and intelligent analysis** (pitch decks, reports, policies) for structured insight extraction
* Provide an **interactive question–answer engine** that dynamically refines responses based on user intent
* Support **translation-aware retrieval**, allowing users to query in one language and retrieve insights from documents in another
* Build a scalable foundation for future intelligent features such as reasoning, recommendation, and trend detection

---

---
### 🧠 System Architecture
![System Architecture](Photos/System architecture.png)

```

```

---

## 🧩 Features

### ✅ Implemented

* 📰 Automated startup news ingestion (TechCrunch, YourStory)
* 🧠 LLM-based information extraction
* 📦 Structured storage (JSON + SQLite)
* 🔍 Semantic search using ChromaDB
* 💬 Conversational RAG interface
* 🧾 Source-cited responses
* 🗂 Metadata-based filtering

### 🚧 In Progress

* 🌐 Multilingual translation support
* 📄 Document upload (PDF / PPT / DOCX)
* 🔁 Duplicate content detection for other three sources(blogs,vc thesis,policy pdfs)
* 🧩 Intelligent follow-up questioning
* 🎨 React + Tailwind UI

---

## 🗂️ Project Structure

```
startup-intelligence-rag/
│
├── data/
│   ├── raw/                # Raw scraped articles
│   ├── processed/          # Structured JSON outputs
│   ├── metadata/           # SQLite metadata DB
│
├── ingestion/
│   ├── fetch_news.py       # RSS-based news ingestion
│   ├── fetch_tech_blogs.py
│   ├── fetch_vc.py
│
├── processing/
│   ├── llm_processing.py   # LLM-based information extraction
│   ├── process_articles.py
│
├── retrieval/
│   ├── rag.py              # Vector DB creation
│   ├── rag_app.py          # Streamlit RAG interface
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Component     | Technology           |
| ------------- | -------------------- |
| LLM           | LLaMA 3 (via Ollama) |
| Embeddings    | Ollama Embeddings    |
| Vector DB     | ChromaDB             |
| Backend       | Python               |
| UI            | Streamlit            |
| Storage       | SQLite               |
| Parsing       | BeautifulSoup        |
| RAG Framework | LangChain            |

---
In Futher implentation we will be using Gemini instead of ollama for better results.

## 🧪 How It Works (Pipeline)

1. **News Ingestion**

   * RSS feeds are scraped
   * Articles cleaned and stored

2. **LLM Processing**

   * Extracts:

     * Summary
     * Key facts
     * Funding info
     * Metadata

3. **Vectorization**

   * Text embedded using LLaMA
   * Stored in ChromaDB

4. **Retrieval**

   * Semantic search retrieves relevant chunks

5. **Generation**

   * LLM generates grounded responses with evidence

---

## ▶️ How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Ollama

```bash
ollama run llama3
```

### 3. Run Ingestion

```bash
python ingestion/fetch_news.py
python processing/process_articles.py
```

### 4. Build Vector Database

```bash
python retrieval/rag.py
```

### 5. Launch Application

```bash
streamlit run retrieval/rag_app.py
```

---

## 🧠 Example Queries

* *“Which startups recently raised Series A funding in India?”*
* *“Show startups related to AI healthcare funding.”*
* *“Which investors are active in fintech?”*

---

## 🛣️ Roadmap

| Feature              | Status |
| -------------------- | ------ |
| News ingestion       | ✅     |
| RAG pipeline         | ✅     |
| Chat history         | ✅     |
| Multilingual support | 🔄     |
| Document upload      | 🔄     |
| UI Dashboard         | 🔄     |
| Duplicate detection  | 🔜     |
| Investor matching    | 🔜     |

## 📸 Project Screenshots

### 🏠 Home / Chat Interface
![Chat Interface](Photos/opimage1.png)

### 🔍 Chat history
![Chat history](Photos/opimage2.png)




