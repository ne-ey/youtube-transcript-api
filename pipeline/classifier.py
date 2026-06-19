"""
pipeline/classifier.py
──────────────────────
Lightweight keyword-based content classifier.
Decoupled from LLM inference — plug-and-play swap ready.

Categories:
  Education | Technology | Business | Health & Fitness |
  Entertainment | Science | Personal Development | Other
"""

from collections import Counter
import re


CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Education": [
        "learn", "tutorial", "course", "lesson", "explain", "study",
        "university", "school", "teach", "lecture", "concept", "understand",
        "how to", "guide", "beginner", "advanced", "exam", "quiz"
    ],
    "Technology": [
        "code", "programming", "software", "hardware", "ai", "machine learning",
        "deep learning", "python", "javascript", "api", "model", "neural",
        "algorithm", "data science", "cloud", "github", "linux", "tech",
        "developer", "framework", "llm", "gpt", "transformer"
    ],
    "Business": [
        "startup", "company", "revenue", "profit", "market", "strategy",
        "entrepreneur", "investment", "stock", "finance", "sales", "marketing",
        "brand", "product", "customer", "growth", "billion", "million"
    ],
    "Health & Fitness": [
        "workout", "exercise", "diet", "nutrition", "health", "fitness",
        "calories", "weight", "muscle", "cardio", "yoga", "meditation",
        "mental health", "therapy", "doctor", "medical", "disease", "sleep"
    ],
    "Entertainment": [
        "funny", "comedy", "movie", "music", "game", "gaming", "anime",
        "reaction", "vlog", "prank", "challenge", "story", "drama",
        "celebrity", "actor", "singer", "video game", "stream"
    ],
    "Science": [
        "research", "experiment", "physics", "chemistry", "biology",
        "space", "nasa", "planet", "quantum", "atom", "theory",
        "hypothesis", "climate", "nature", "evolution", "species"
    ],
    "Personal Development": [
        "motivation", "success", "habit", "mindset", "productivity",
        "goal", "confidence", "discipline", "focus", "self", "growth",
        "journal", "routine", "positive", "inspire", "life", "advice"
    ],
}


def classify_content(transcript: str) -> str:
    """
    Classify transcript into a content category using keyword matching.
    Returns the category with the highest keyword hit count.
    """
    text = transcript.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    words = text.split()
    word_set = set(words)

    scores: Counter = Counter()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if " " in kw:
                if kw in text:
                    scores[category] += 2
            else:
                if kw in word_set:
                    scores[category] += 1

    if not scores:
        return "Other"

    return scores.most_common(1)[0][0]
