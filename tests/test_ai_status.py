# Run from project root:
# PYTHONPATH=. python tests/test_ai_status.py

from ai_tools.status_tool import get_latest_status
from ai_tools.ai_client import ask_ai

status = get_latest_status(1)

answer = ask_ai(f"""
Explain this latest heat pump status:

{status}
""")

print(answer)
