# def build_prompt(persona, customer, memory, kb_chunks, user_input, tone):
#     return f"""{persona}

# Customer Info:
# - Name: {customer.get("name")}
# - Due: ₹{customer.get("premium_amount")} on {customer.get("due_date")}
# - Policy Term: {customer.get("policy_term")} years
# - Preferred Payment Mode: {customer.get("payment_mode")}
# - Tone Detected: {tone}

# Recent Conversation:
# {memory}

# User just said: "{user_input}"

# Relevant Knowledge:
# {kb_chunks}

# As Veena, respond empathetically and clearly. Ask gentle follow-up questions. Help Ravi continue his policy without pressure.
# """

# ============================================
# prompt_builder.py — for Gemini prompt format
# ============================================

# engine/prompt_builder.py

from prompts.veena_agent import load_veena_persona

def personalize(text: str, customer: dict) -> str:
    for key, value in customer.items():
        text = text.replace(f"[{key}]", str(value))
    return text

def build_prompt(customer, memory, kb_chunks, user_input, tone):
    persona = load_veena_persona()

    prompt = f"""{persona}

📌 Customer Profile:
- Name: {customer.get("name")}
- Premium Due: ₹{customer.get("premium_amount")} on {customer.get("due_date")}
- Policy Term: {customer.get("policy_term")} years
- Payment Mode: {customer.get("payment_mode")}
- Detected Sentiment: {tone}

🧠 Recent Conversation:
{memory}

👂 User just said: "{user_input}"

📚 Relevant Knowledge:
{kb_chunks}

🎯 Instruction:
Reply naturally, kindly, and convincingly as Veena. Encourage payment or support decision-making. Never break character.
"""
    return prompt
