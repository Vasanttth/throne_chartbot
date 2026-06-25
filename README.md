# 🛋️ Throne Recliners Chatbot

An AI-powered RAG (Retrieval-Augmented Generation) chatbot for
[Throne Recliners](https://thronerecliners.in) — built with Python,
LangChain, ChromaDB, Ollama, and Streamlit.

---

## 🏗️ Architecture

```
data/*.txt
   │
   ▼
[ingest.py]  →  HuggingFace Embeddings  →  ChromaDB (vectorstore/)
                                                  │
User Question ────────────────────────────────────┤
   │                                              ▼
   │                                    Similarity Search (top-4 chunks)
   │                                              │
   └──────────► Ollama LLM (llama3.2) ◄──────────┘
                      │
                      ▼
              Answer + Sources
                      │
                      ▼
              Streamlit Chat UI
```

---

## 📁 Project Structure

```
throne-chatbot/
├── app.py           # Streamlit UI (dark royal theme)
├── chatbot.py       # RAG chain (retrieval + LLM + memory)
├── ingest.py        # One-time data indexing script
├── requirements.txt
├── README.md
└── data/
    └── throne_recliners_knowledge_base.txt   # Your dataset
```

---

## ⚙️ Setup & Installation

### Step 1 — Install Ollama
Download from https://ollama.com and install, then:
```bash
ollama serve              # Start the Ollama server
ollama pull llama3.2      # Download the LLM (~2 GB)
```

### Step 2 — Create Python virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Index your data (run once)
```bash
python ingest.py
```
This loads `data/*.txt`, splits into chunks, embeds them with
`all-MiniLM-L6-v2`, and saves to `vectorstore/`.

### Step 5 — Launch the chatbot
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

---

## ➕ Adding More Data

1. Drop any `.txt` or `.pdf` file into the `data/` folder.
2. Re-run `python ingest.py` to re-index.
3. Restart the Streamlit app.

---

## 🔧 Configuration

| Setting | File | Default |
|---|---|---|
| Ollama model | `chatbot.py` → `OLLAMA_MODEL` | `llama3.2` |
| Chunk size | `ingest.py` → `chunk_size` | `400` |
| Retrieved chunks | `chatbot.py` → `k` | `4` |
| Memory window | `chatbot.py` → `k=6` | `6 turns` |
| Embedding model | both files → `EMBED_MODEL` | `all-MiniLM-L6-v2` |

### Alternative Ollama models
```bash
ollama pull mistral       # Faster, lighter
ollama pull gemma2        # Google's model
ollama pull phi3          # Very small, good for low RAM
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `vectorstore not found` | Run `python ingest.py` first |
| `Connection refused` (Ollama) | Run `ollama serve` in a terminal |
| `Model not found` | Run `ollama pull llama3.2` |
| Slow responses | Try `phi3` or `mistral` for faster inference |
| Wrong answers | Increase `chunk_size` to `600` in `ingest.py` and re-index |

---

## 📞 About Throne Recliners

- **Website:** https://thronerecliners.in
- **Location:** Thoothukudi, Tamil Nadu, India
- **IndiaMART:** https://www.indiamart.com/thronerecliners/
