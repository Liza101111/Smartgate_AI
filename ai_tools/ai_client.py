import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv("/home/sct/smartgate/config.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

with open("/home/sct/smartgate/prompts/system_prompt.txt") as f:
    SYSTEM_PROMPT = f.read()


def ask_ai(user_prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
