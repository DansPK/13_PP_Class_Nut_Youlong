"""Ask the pipeline 5 test questions (1 off-topic) and print the answers."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

from dotenv import load_dotenv
load_dotenv()

from generate import generate_answer

QUESTIONS = [
    "How do I reset a forgotten PIN?",
    "How do I configure VPN access as a remote worker?",
    "What should I do if the printer is jammed?",
    "How do I set up a conference call on Cisco Webex?",
    "What is the CEO's home address?",  # off-topic, not in any document
]

for question in QUESTIONS:
    answer, _, chunks = generate_answer(question)
    print(f"Q: {question}")
    print(f"A: {answer}")
    print(f"sources: {[c['source'] for c in chunks]}")
    print()
