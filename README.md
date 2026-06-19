# 🎬 YouTube Transcript Intelligence Engine

> **NLP Pipeline · Google Gemini Pro API · Streamlit UI**

A full-stack NLP application that extracts, analyzes, and summarizes YouTube video transcripts using Google Gemini Pro LLM — with a modular, plug-and-play architecture.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📥 **Transcript Ingestion** | Fetches transcripts via `youtube-transcript-api` |
| 🖼️ **Media-Aware UI** | Renders CDN thumbnails alongside results |
| 🏷️ **Content Classification** | NLP keyword classifier (8 categories, no API needed) |
| 🤖 **Gemini Pro Inference** | Summarize, Key Takeaways, Q&A, Sentiment, Topic Analysis |
| 🔌 **Plug-and-Play LLM Layer** | Swap models without changing application logic |
| 🎨 **Streamlit UI** | Clean, dark-themed responsive interface |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/youtube-transcript-engine.git
cd youtube-transcript-engine
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your Gemini API Key

- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a free API key (no billing needed for basic usage)

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🧠 How to Use

1. **Open the app** → it launches at `http://localhost:8501`
2. **Paste your Gemini API Key** in the left sidebar
3. **Choose a task** — Summarize / Key Takeaways / Q&A / Sentiment / Topic Classification
4. **Paste any YouTube URL** in the main input box
5. **Click Analyze** → the pipeline runs in 3 stages:
   - Transcript fetched → content classified → Gemini Pro inference
6. **View results** + raw transcript in the expander

---

## 🗂️ Project Structure

```
youtube-transcript-engine/
│
├── app.py                    # Main Streamlit UI
│
├── pipeline/
│   ├── __init__.py
│   ├── ingestion.py          # Video ID extraction, transcript fetch, metadata
│   ├── classifier.py         # NLP keyword-based content classification
│   └── inference.py          # Gemini Pro prompt builder + LLM inference
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔌 Architecture — Modular Prompt Layer

The inference layer is **fully decoupled** from the model:

```python
# pipeline/inference.py
MODEL_NAME = "gemini-1.5-flash"   # ← change this ONE line to swap models
```

- Swap to `gemini-1.5-pro`, `gemini-2.0-flash`, or any future model
- The `build_prompt()` and `run_inference()` functions stay unchanged
- Application logic is **model-agnostic**

---

## 📊 Supported Tasks

| Task | Description |
|---|---|
| **Summarize** | 3–5 sentence abstract summary |
| **Key Takeaways** | Numbered list of 5–7 insights |
| **Q&A** | Ask any question about the video |
| **Sentiment Analysis** | Tone, emotion, sentiment breakdown |
| **Topic Classification** | Domain, sub-topics, target audience, tags |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Streamlit** — UI framework
- **youtube-transcript-api** — Transcript ingestion
- **Google Generative AI SDK** — Gemini Pro inference
- **Regex + Counter** — Lightweight NLP classifier

---

## ⚠️ Limitations

- Only works for videos with captions/transcripts enabled
- Gemini free tier has rate limits (15 req/min)
- Auto-generated captions may have transcription errors

---

## 👩‍💻 Author

**Neha Pandey**  
B.Tech CSE (AI/ML) · United College of Engineering and Research, Prayagraj  
[GitHub](https://github.com/YOUR_USERNAME) · [Portfolio](https://nehapandey-portfolio-web.vercel.app)

---

## 📄 License

MIT License — free to use and modify.
