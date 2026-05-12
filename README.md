# 🧠 Voz Forum RAG Chatbot

Hệ thống Retrieval-Augmented Generation (RAG) dạng đồ thị (graph-based), xây dựng để phân tích và trả lời câu hỏi từ dữ liệu thảo luận thực tế trên diễn đàn Voz.vn bằng tiếng Việt.

---

## 📌 Tổng Quan

Project triển khai một pipeline AI đầu cuối gồm:

1. Thu thập dữ liệu từ diễn đàn Voz.vn (web scraping)
2. Làm sạch và tiền xử lý văn bản tiếng Việt
3. Phân tích dữ liệu khám phá (EDA)
4. Xây dựng hệ thống RAG lai (vector search + knowledge graph)
5. Giao diện hội thoại đa lượt với bộ nhớ ngữ cảnh

Người dùng có thể đặt câu hỏi tự nhiên như:
- *"Mọi người nói gì về vấn đề kinh tế?"*
- *"Quan điểm chung về chủ đề đó là gì?"*
- *"Tiếp tục nói thêm về điều đó"* ← hệ thống hiểu ngữ cảnh từ lượt trước

---

## 🏗️ Kiến Trúc Hệ Thống

```
Voz.vn Forum
     │
     ▼
[Web Scraping]          BeautifulSoup + Cloudscraper
     │
     ▼
[Raw CSV Dataset]       Dữ liệu thô: user, content, reply, thread
     │
     ▼
[Preprocessing]         Làm sạch, stopword, định dạng ngữ cảnh
     │
     ▼
[EDA]                   Phân tích tần suất từ, WordCloud, chủ đề
     │
     ▼
[LightRAG Indexing]     Embedding → Vector DB + Knowledge Graph (Neo4j)
     │
     ▼
[FastAPI Backend]       Xử lý query, session memory, hybrid retrieval
     │
     ▼
[Streamlit UI]          Giao diện chat đa lượt
```

---

## ⚙️ Chế Độ Truy Vấn

LightRAG hỗ trợ 4 chế độ truy vấn, có thể chọn trực tiếp trên giao diện:

| Chế độ | Mô tả |
|--------|-------|
| `local` | Tìm kiếm theo ngữ nghĩa cục bộ, phù hợp câu hỏi cụ thể |
| `global` | Tổng hợp thông tin toàn bộ đồ thị, phù hợp câu hỏi tổng quan |
| `hybrid` | Kết hợp local + global, cân bằng tốt nhất |
| `naive` | Vector search thuần túy, không dùng graph |

---

## 🛠️ Công Nghệ Sử Dụng

| Thành phần | Công nghệ |
|---|---|
| Web scraping | `BeautifulSoup`, `Cloudscraper` |
| Xử lý dữ liệu | `Pandas`, `Regex` |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| LLM | ZhipuAI GLM-4-Flash |
| RAG framework | `LightRAG` |
| Graph database | `Neo4j` |
| API backend | `FastAPI` + `Uvicorn` |
| Frontend | `Streamlit` |
| Notebooks | Jupyter / Google Colab |

---

## 📂 Cấu Trúc Thư Mục

```
LightRAG/
├── lightrag/                  # Core LightRAG library
│   ├── __init__.py
│   ├── lightrag.py            # Main RAG engine
│   ├── llm.py                 # LLM integrations
│   ├── operate.py             # Graph operations
│   ├── prompt.py              # Prompt templates
│   ├── storage.py             # Storage backends
│   ├── utils.py               # Utilities
│   └── kg/                    # Knowledge graph backends
│       ├── neo4j_impl.py
│       ├── chroma_impl.py
│       └── ...
├── lib/                       # Frontend JS/CSS libraries
├── image/                     # Ảnh minh họa cho README
├── notebooks/
│   ├── ScrapeData.ipynb       # Pipeline thu thập dữ liệu
│   └── FINAL_NOTEBOOK.ipynb   # Toàn bộ pipeline RAG
├── app.py                     # Streamlit frontend
├── server.py                  # FastAPI backend
├── requirements.txt
├── .env.example               # Mẫu biến môi trường
├── .gitignore
└── LICENSE
```

---

## 🚀 Hướng Dẫn Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.9+
- Neo4j 5.x (hoặc dùng Neo4j AuraDB free tier)
- RAM tối thiểu 8GB (do load embedding model local)

### 1. Clone và cài dependencies

```bash
git clone <repo-url>
cd LightRAG
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường

```bash
cp .env.example .env
```

Chỉnh sửa file `.env`:

```env
ZHIPU_API_KEY=your_zhipuai_api_key
WORKING_DIR=./workdir
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

> 🔑 Lấy ZhipuAI API key tại: https://open.bigmodel.cn

### 3. Khởi động Neo4j

```bash
# Nếu dùng Docker:
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:5
```

### 4. Chạy Backend (FastAPI)

```bash
python server.py
# API chạy tại: http://localhost:8000
```

### 5. Chạy Frontend (Streamlit)

```bash
streamlit run app.py
# UI chạy tại: http://localhost:8501
```

---

## 📊 Thu Thập & Chuẩn Bị Dữ Liệu

Xem notebook `notebooks/ScrapeData.ipynb` để:
- Cào dữ liệu từ Voz.vn (hỗ trợ bypass Cloudflare)
- Xuất ra file CSV có cấu trúc

Sau đó xem `notebooks/FINAL_NOTEBOOK.ipynb` để:
- Tiền xử lý và EDA
- Insert dữ liệu vào LightRAG
- Kiểm thử các chế độ truy vấn

---

## 🔗 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/chatbot/` | Gửi câu hỏi, nhận trả lời |

**Request body:**
```json
{
  "text": "Mọi người nghĩ gì về vấn đề X?",
  "mode": "hybrid"
}
```

**Response:**
```json
{
  "response": "Dựa trên các cuộc thảo luận trên Voz..."
}
```

---

## ⚠️ Lưu Ý

- **Session memory** hiện được lưu in-memory, sẽ mất khi restart server. Với môi trường production, nên dùng Redis.
- Lần chạy đầu tiên sẽ tải embedding model (~90MB), cần kết nối internet.
- Dữ liệu Voz.vn chỉ dùng cho mục đích nghiên cứu và học thuật.

---

## 📄 License

MIT License — xem file [LICENSE](./LICENSE)
