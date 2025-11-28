# 🤖 Agentic Compliance Checker (RAG)

An AI-powered legal audit system that uses **Retrieval-Augmented Generation (RAG)** to automatically review commercial contracts against corporate compliance rules. Built with **Google Gemini 2.5**, **LangChain**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-v0.2-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📖 Project Overview

This system solves the “needle in a haystack” problem for legal and compliance teams.

Users upload a PDF contract and the **Compliance Agent**:

1. **Ingests** the PDF using semantic chunking  
2. **Retrieves** relevant clauses via vector search (ChromaDB)  
3. **Audits** content against **15 corporate compliance rules**  
4. **Generates** a CSV report with:  
   - `PASS` / `FAIL`  
   - Quoted evidence  
   - Recommended remediation steps  

---

## ✨ Key Features

### ⚡ Dual Rate-Limiting Engine  
Ensures stable performance even on the **Free Gemini API Tier**:

- **Chat Model:** 10 requests/min  
- **Embeddings:** 100 requests/min  

### 🧠 Smart Legal Reasoning  
Powered by **Gemini 2.5 Flash**, capable of distinguishing legal intent, not just keywords.

### 📊 Full UI Dashboard  
Streamlit interface with color-coded results, clause highlights, and CSV export.

### 📂 Standardized Architecture  
Clean separation of data, config, UI, and logic.

---

## 🛠️ Tech Stack

- **LLM:** Gemini 2.5 Flash  
- **Embeddings:** `text-embedding-004`  
- **Framework:** LangChain  
- **Vector Store:** ChromaDB  
- **Frontend:** Streamlit  
- **PDF Processing:** `pypdf`, `pandas`  

---

## 📂 Project Structure


```text
compliance-rag/
├── .env                    # API Keys (Not committed)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── data/
│   ├── raw_pdfs/           # PDF inputs
│   └── chroma_db/          # Vector store persistence
└── src/
    ├── config.py           # Compliance Rules (15 definitions)
    ├── rate_limiter.py     # Custom Dual-Rate Limiter class
    └── main_app.py         # Main Streamlit Application
```

---
## Setup & Installation
1. Clone the Repository
git clone 
cd compliance-rag

## Create a Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate

## Install Dependencies
pip install -r requirements.txt

## Configure API Keys

Create a .env file in the root directory:

GOOGLE_API_KEY=AIzaSy...YourKeyHere

## Usage

Run the Streamlit application:

streamlit run src/main_app.py


The UI opens automatically at:
http://localhost:8501

## Workflow:

Upload a PDF

Click Run Compliance Audit

Review results

Download compliance_report.csv

