import streamlit as st
from pipeline.ingestion import extract_video_id, fetch_transcript, get_video_metadata
from pipeline.classifier import classify_content
from pipeline.inference import run_inference

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Transcript Intelligence Engine",
    page_icon="🎬",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF4B4B;
    }
    .subtitle {
        font-size: 1rem;
        color: #888;
        margin-bottom: 1.5rem;
    }
    .tag {
        background-color: #1E1E2E;
        color: #CDD6F4;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 6px;
    }
    .result-box {
        background-color: #0E1117;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .section-header {
        color: #FF4B4B;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🎬 YouTube Transcript Intelligence Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">NLP Pipeline · Google Gemini Pro · Streamlit UI</div>', unsafe_allow_html=True)
st.markdown(
    '<span class="tag">Python</span>'
    '<span class="tag">Gemini Pro API</span>'
    '<span class="tag">NLP</span>'
    '<span class="tag">Streamlit</span>',
    unsafe_allow_html=True
)
st.markdown("---")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    gemini_api_key = st.text_input("🔑 Gemini API Key", type="password", placeholder="Paste your API key here")

    st.markdown("---")
    st.subheader("🔧 Inference Mode")
    task = st.selectbox(
        "Select Task",
        ["Summarize", "Key Takeaways", "Q&A", "Sentiment Analysis", "Topic Classification"]
    )

    if task == "Q&A":
        user_question = st.text_input("❓ Your Question", placeholder="Ask anything about the video...")
    else:
        user_question = None

    st.markdown("---")
    st.markdown("**Built by:** Neha Pandey")
    st.markdown("**Stack:** Python · Streamlit · Gemini Pro · youtube-transcript-api")

# ── Main Input ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    url = st.text_input("🔗 YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Analyze", use_container_width=True)

# ── Pipeline Execution ────────────────────────────────────────────────────────
if run_btn:
    if not gemini_api_key:
        st.error("❌ Please enter your Gemini API Key in the sidebar.")
        st.stop()
    if not url:
        st.error("❌ Please enter a YouTube URL.")
        st.stop()

    video_id = extract_video_id(url)
    if not video_id:
        st.error("❌ Could not extract Video ID. Please check the URL.")
        st.stop()

    # ── Step 1: Fetch Transcript ──────────────────────────────────────────────
    with st.spinner("📥 Fetching transcript..."):
        transcript, error = fetch_transcript(video_id)

    if error:
        st.error(f"❌ Transcript Error: {error}")
        st.stop()

    # ── Step 2: Video Metadata + Thumbnail ───────────────────────────────────
    metadata = get_video_metadata(video_id)

    col_thumb, col_meta = st.columns([1, 2])
    with col_thumb:
        st.image(metadata["thumbnail"], use_container_width=True)
    with col_meta:
        st.markdown(f"### 🎥 {metadata['title']}")
        st.markdown(f"**Video ID:** `{video_id}`")
        st.markdown(f"**Transcript Length:** `{len(transcript.split())} words`")

        # ── Step 3: Classify ──────────────────────────────────────────────────
        with st.spinner("🏷️ Classifying content..."):
            category = classify_content(transcript)
        st.markdown(f"**Detected Category:** `{category}`")

    st.markdown("---")

    # ── Step 4: LLM Inference ─────────────────────────────────────────────────
    with st.spinner(f"🤖 Running Gemini Pro → {task}..."):
        result = run_inference(
            transcript=transcript,
            task=task,
            api_key=gemini_api_key,
            question=user_question
        )

    st.markdown(f'<div class="section-header">📋 {task} Result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    # ── Raw Transcript Expander ───────────────────────────────────────────────
    with st.expander("📄 View Raw Transcript"):
        st.text_area("Transcript", transcript, height=300)
