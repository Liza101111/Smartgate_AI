import logging
import os
import re
from datetime import datetime
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

from ai_tools.db_tool import run_query

_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(_ROOT / "config.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (_ROOT / "prompts" / "system_prompt.txt").read_text(encoding="utf-8")

_MAX_ROUNDS = 5
_QUERY_PATTERN = re.compile(r"^QUERY:\s*(.+)$", re.MULTILINE)

log = logging.getLogger(__name__)


def ask_ai(user_prompt: str) -> str:
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    day_str = now.strftime('%A')
    context = f"Current date and time: {now_str} ({day_str})\n\n{user_prompt}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": context},
    ]

    for round_num in range(_MAX_ROUNDS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )

        text = response.choices[0].message.content

        match = _QUERY_PATTERN.search(text)
        if not match:
            log.debug(f"No SQL query in response (round {round_num + 1})")
            return text

        sql = match.group(1).strip()
        log.debug(f"Generated SQL (round {round_num + 1}): {sql}")

        try:
            result = run_query(sql)
            result_str = str(result)
            log.debug(f"Query result: {len(result)} rows")
        except ValueError as e:
            result_str = f"SQL syntax error: {e}\nPlease fix the query."
            log.warning(f"SQL error (round {round_num + 1}): {e}")
        except Exception as e:
            result_str = f"Database error: {e}\nPlease try a different query."
            log.error(f"Database error (round {round_num + 1}): {e}")

        messages.append({"role": "assistant", "content": text})
        messages.append(
            {
                "role": "user",
                "content": f"Query result:\n{result_str}\n\nNow provide your final answer based on this data.",
            }
        )

    log.warning(f"Failed to answer question after {_MAX_ROUNDS} rounds")
    return "I was unable to answer the question after several attempts."
