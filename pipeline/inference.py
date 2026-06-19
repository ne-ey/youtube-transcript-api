"""
pipeline/inference.py
──────────────────────
Modular prompt layer for LLM inference using Google Gemini Pro.

Design:
  - Task-specific prompt builder (decoupled from model)
  - Model swap = change 1 line (plug-and-play architecture)
  - Supports: Summarize | Key Takeaways | Q&A | Sentiment | Topic Classification
"""

from google import genai
from google.genai import types

# ── Model Config (swap here for different LLMs) ───────────────────────────────
MODEL_NAME = "gemini-2.0-flash"
MAX_TRANSCRIPT_CHARS = 12000  # trim for speed


def build_prompt(transcript: str, task: str, question: str | None = None) -> str:
    """
    Build a structured prompt based on the selected task.
    Decoupled from the model — swap models without changing this layer.
    """
    trimmed = transcript[:MAX_TRANSCRIPT_CHARS]
    base = f"You are an expert content analyst. Below is a YouTube video transcript:\n\n---\n{trimmed}\n---\n\n"

    prompts = {
        "Summarize": (
            base +
            "Task: Write a concise, well-structured abstract summary of this video in 3–5 sentences. "
            "Focus on the core message, key ideas, and takeaways. Be direct and informative."
        ),
        "Key Takeaways": (
            base +
            "Task: Extract the top 5–7 key takeaways from this video. "
            "Format as a numbered list. Each point should be specific, actionable, and insightful."
        ),
        "Q&A": (
            base +
            f"Task: Answer the following question based ONLY on the transcript content:\n\n"
            f"Question: {question or 'What is this video about?'}\n\n"
            "Provide a detailed, accurate answer. If the answer is not in the transcript, say so."
        ),
        "Sentiment Analysis": (
            base +
            "Task: Analyze the overall sentiment and tone of this video. Include:\n"
            "1. Overall sentiment (Positive / Negative / Neutral / Mixed)\n"
            "2. Dominant emotions detected\n"
            "3. Speaker's tone (e.g., enthusiastic, critical, calm, motivational)\n"
            "4. A brief justification with examples from the transcript."
        ),
        "Topic Classification": (
            base +
            "Task: Perform a detailed topic analysis. Include:\n"
            "1. Primary topic/domain\n"
            "2. Sub-topics covered\n"
            "3. Target audience\n"
            "4. Estimated knowledge level required (Beginner / Intermediate / Advanced)\n"
            "5. Tags/keywords (comma-separated)"
        ),
    }

    return prompts.get(task, prompts["Summarize"])


def run_inference(
    transcript: str,
    task: str,
    api_key: str,
    question: str | None = None
) -> str:
    """
    Run LLM inference using Google Gemini (new google-genai SDK).
    Returns the model's response as a string.
    """
    try:
        client = genai.Client(api_key=api_key)
        prompt = build_prompt(transcript, task, question)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=1024,
            ),
        )

        return response.text

    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "invalid" in error_msg.lower() or "api key" in error_msg.lower():
            return "❌ Invalid API Key. Please check your Gemini API key in the sidebar."
        elif "quota" in error_msg.lower():
            return "❌ API quota exceeded. Please check your Gemini API usage limits."
        else:
            return f"❌ Gemini API Error: {error_msg}"
