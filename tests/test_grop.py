# Run from project root:
# PYTHONPATH=. python tests/test_grop.py

from ai_tools.ai_client import ask_ai

answer = ask_ai("Explain SmartGate AI in one simple sentence.")

print(answer)
