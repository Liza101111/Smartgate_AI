import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(_ROOT / "config.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


SYSTEM_PROMPT = (_ROOT / "prompts" / "system_prompt.txt").read_text(encoding="utf-8")


def ask_ai(user_prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
