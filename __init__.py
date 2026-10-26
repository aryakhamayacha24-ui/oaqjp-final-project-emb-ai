cd /home/project

mkdir -p EmotionDetection

cat > EmotionDetection/__init__.py <<'PY'
"""Emotion Detection package."""

from . import emotion_detection
PY

cat > EmotionDetection/emotion_detection.py <<'PY'
import requests


def emotion_detector(text_to_analyze):
    """Analyze text and return its detected emotions."""
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 400:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            }

        response.raise_for_status()
        data = response.json()

        emotions = data["emotionPredictions"][0]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)

        return {
            "anger": emotions.get("anger"),
            "disgust": emotions.get("disgust"),
            "fear": emotions.get("fear"),
            "joy": emotions.get("joy"),
            "sadness": emotions.get("sadness"),
            "dominant_emotion": dominant_emotion,
        }

    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }
PY
