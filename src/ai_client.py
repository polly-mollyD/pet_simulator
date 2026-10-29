import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


def generate_reply(messages):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "Add GEMINI_API_KEY to .env, then restart the app."
        )

    with OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        timeout=30.0,
        max_retries=0,
    ) as client:
        response = client.chat.completions.create(
            model="gemini-3.1-flash-lite",
            messages=messages,
        )

    reply = (response.choices[0].message.content or "").strip()

    if not reply:
        raise RuntimeError("Gemini returned no text.")

    return reply