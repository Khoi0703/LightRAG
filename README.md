Dưới đây là **README đầy đủ – chi tiết – chuyên nghiệp – đủ sâu để đưa lên GitHub portfolio AI/Data**.
Bạn chỉ cần copy vào `README.md`.

---

# 🧠 Voz Forum Conversational RAG System

A Graph-Based Conversational Retrieval-Augmented Generation (RAG) system built to analyze, retrieve, and answer questions from real-world Vietnamese forum discussions.

---

# 📌 Overview

This project builds an end-to-end AI pipeline that:

1. Scrapes discussion threads from the Voz.vn forum
2. Cleans and preprocesses textual data
3. Performs exploratory data analysis (EDA)
4. Constructs a hybrid Retrieval-Augmented Generation (RAG) system
5. Integrates vector search and knowledge graph retrieval
6. Enables conversational question answering over scraped forum data

The system allows users to ask natural language questions such as:

* “How do users talk about America?”
* “What is that country?”
* “What opinions do people have about economic issues?”

And receive context-aware answers grounded in real forum discussions.

---

# 🎯 Project Objectives

* Build a scalable web scraping pipeline
* Perform text preprocessing and exploratory analysis
* Design a hybrid retrieval system (vector + graph)
* Implement conversational memory
* Integrate LLM-based response generation
* Demonstrate practical LLM application in real-world data

---

# 🏗️ System Architecture

## 1️⃣ Data Collection Layer

* Web scraping from Voz.vn forum
* Bypassing Cloudflare protection
* Parsing HTML threads and comments
* Extracting:

  * Thread title
  * User
  * Comment content
  * Reply relationships

Output: Structured CSV dataset

---

## 2️⃣ Data Processing Layer

* Text cleaning
* Removing noise and special characters
* Stopword filtering
* Formatting contextual data:

  ```
  User: ...
  Reply: ...
  Reply to comment: ...
  About this topic: ...
  ```

This structured format improves embedding quality and contextual reasoning.

---

## 3️⃣ Exploratory Data Analysis (EDA)

* Word frequency analysis
* WordCloud visualization
* Identifying trending topics
* Understanding discussion patterns

Purpose:

* Validate data quality
* Extract high-level insights
* Guide downstream modeling

---

## 4️⃣ Retrieval-Augmented Generation (RAG)

The core of this project is a hybrid RAG system powered by:

* Embedding generation
* Vector similarity search
* Knowledge graph-based retrieval
* Conversational history memory

### Retrieval Modes

* Vector-based semantic search
* Graph-based relational search
* Hybrid retrieval (combining both)

---

## 5️⃣ Conversational Layer

The system supports:

* Multi-turn conversation
* Context retention
* Follow-up question understanding
* Coreference resolution

Example:

User:

> How do people talk about America?

User (follow-up):

> What is that country?

The system understands that “that country” refers to “America” from prior context.

---

# 🛠️ Tech Stack

## Programming Language

* Python

## Data Collection

* BeautifulSoup
* Cloudscraper

## Data Processing

* Pandas
* Regex
* NumPy

## Visualization

* Matplotlib
* WordCloud

## AI & Retrieval

* LightRAG
* LLM API
* Embedding Models
* Vector Retrieval
* Knowledge Graph Integration

## Environment

* Jupyter Notebook
* Google Colab

---

# 🔄 Project Pipeline

```
Web Scraping
      ↓
Raw HTML Parsing
      ↓
Structured CSV Dataset
      ↓
Text Cleaning & Formatting
      ↓
EDA & Visualization
      ↓
Embedding Generation
      ↓
Vector + Graph Storage
      ↓
Hybrid Retrieval
      ↓
Conversational AI Response
```

---

# 📂 Project Structure

```
├── ScrapeData.ipynb          # Data collection pipeline
├── FINAL_NOTEBOOK.ipynb      # RAG system implementation
├── know_voz_think.csv        # Processed dataset
├── voz_complete_data.csv     # Raw scraped data
└── README.md
```

---

# 🧠 Key Technical Concepts Demonstrated

* Web scraping under Cloudflare protection
* Text preprocessing for LLM pipelines
* Embedding-based semantic search
* Vector database retrieval
* Knowledge graph-based context modeling
* Hybrid retrieval strategy
* Conversational RAG design
* Multi-turn dialogue handling

---

# 🚀 How to Run

## 1️⃣ Install Dependencies

```bash
pip install pandas beautifulsoup4 cloudscraper matplotlib wordcloud lightrag
```

---

## 2️⃣ Run Scraping Notebook

Open:

```
ScrapeData.ipynb
```

This will:

* Crawl forum data
* Save results as CSV

---

## 3️⃣ Run RAG System

Open:

```
FINAL_NOTEBOOK.ipynb
```

This will:

* Load dataset
* Insert into RAG system
* Enable conversational querying

---


