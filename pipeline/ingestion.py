"""
pipeline/ingestion.py
─────────────────────
Handles:
  - YouTube video ID extraction from URL
  - Transcript fetching via youtube-transcript-api
  - Video metadata + thumbnail via CDN
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from various URL formats:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - https://youtube.com/shorts/VIDEO_ID
    """
    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_transcript(video_id: str) -> tuple[str, str | None]:
    """
    Fetch and concatenate transcript text for a given video ID.
    Returns (transcript_text, error_message).
    error_message is None on success.
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id)
        full_text = " ".join([snippet.text for snippet in fetched])
        return full_text, None
    except Exception as e:
        error_msg = str(e)
        if "disabled" in error_msg.lower():
            return "", "Transcripts are disabled for this video."
        elif "no transcript" in error_msg.lower() or "Could not retrieve" in error_msg:
            return "", "No transcript found. The video may not have captions enabled."
        else:
            return "", f"Could not fetch transcript: {error_msg}"


def get_video_metadata(video_id: str) -> dict:
    """
    Returns basic metadata for a YouTube video.
    Uses YouTube CDN thumbnail (no API key needed).
    Title is fetched via oEmbed (no key required).
    """
    import urllib.request
    import json

    thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    title = f"YouTube Video ({video_id})"
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        with urllib.request.urlopen(oembed_url, timeout=5) as resp:
            data = json.loads(resp.read())
            title = data.get("title", title)
    except Exception:
        pass  # fallback to default title

    return {
        "video_id": video_id,
        "title": title,
        "thumbnail": thumbnail,
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }
