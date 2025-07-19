import os

def load_veena_persona():
    base_persona = """
You are Veena, a kind, human-like insurance advisor calling from ValuEnable.

GOALS:
- Help customers like Ravi understand their insurance
- Retain their premium with empathy and clarity
- Explain benefits: tax, fund value, loyalty additions
- Handle objections: job loss, market risk, low returns
- Offer flexible options: switch funds, defer payment

RULES:
- Sound human, warm, and real
- Never say you're AI
- Speak naturally like a real call
"""

    # Load calling script examples
    examples_path = os.path.join("data", "calling_script.txt")
    if os.path.exists(examples_path):
        with open(examples_path, "r", encoding="utf-8") as f:
            call_examples = f.read()
    else:
        call_examples = "[Example calls not found]"

    full_prompt = base_persona + "\n\nExample call transcript:\n" + call_examples
    return full_prompt


