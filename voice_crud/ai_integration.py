from google import genai
import os
import json
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

api_key = os.getenv("api_key")
client = genai.Client(api_key=api_key)



def sentiment_and_category(feedback_text):
    if client is None:
        return {"sentiment": "unknown", "category": "other"}

    prompt = f"""
    Read this student feedback and classify it.

    Feedback: {feedback_text}

    Return only JSON in this format:
    {{"sentiment": "positive", "category": "faculty"}}

    Sentiment must be: positive, negative, neutral, or unknown.
    Category must be: faculty, academics, infrastructure,
    administration, facilities, or other.
    """

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    result = json.loads(response.text)
    return {
        "sentiment": result.get("sentiment", "unknown"),
        "category": result.get("category", "other"),
    }
