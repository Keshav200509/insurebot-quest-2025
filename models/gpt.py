# import os
# from openai import OpenAI, RateLimitError, APIError
# from dotenv import load_dotenv

# load_dotenv()

# _api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=_api_key) if _api_key else None

# FALLBACK_REPLY = (
#     "I’m sorry, I’m having trouble accessing detailed information right now. "
#     "Please give me a moment, or you can reach our human support line at 1800‑123‑456."
# )

# def chat_completion(system_prompt: str, user_input: str, model: str = "gpt-3.5-turbo") -> str:
#     """Single‑turn chat completion with automatic fallback on API failure."""
#     if client is None:
#         return FALLBACK_REPLY
#     try:
#         res = client.chat.completions.create(
#             model=model,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_input},
#             ],
#             timeout=10,
#         )
#         return res.choices[0].message.content.strip()
#     except (RateLimitError, APIError):
#         return FALLBACK_REPLY

# =====================================
# FILE: models/gpt.py
# PURPOSE: Gemini Chat API Wrapper
# =====================================

# =============================================
# gpt.py — Gemini Pro integration with fallback
# =============================================

# =============================================
# models/gpt.py — FIXED for Gemini Pro v1
# =============================================

# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# FALLBACK_REPLY = (
#     "I’m sorry, I’m currently unable to access the assistant. "
#     "Please try again shortly or reach support at 1800‑123‑456."
# )

# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     print("[Error] Gemini API key missing.")

# model = genai.GenerativeModel("gemini-pro")

# # Use proper chat session for Gemini Pro
# def chat_completion(system_prompt, user_input, model_name="gemini-pro"):
#     try:
#         chat_session = model.start_chat(history=[])
#         full_prompt = f"{system_prompt.strip()}\n\nUser: {user_input.strip()}\nAssistant:"
#         response = chat_session.send_message(full_prompt)
#         return response.text.strip()
#     except Exception as e:
#         print("[Gemini Error]", e)
#         return FALLBACK_REPLY

import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
import os
from dotenv import load_dotenv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex_credentials.json"
load_dotenv()

FALLBACK_REPLY = (
    "I’m sorry, I’m currently unable to access Gemini Pro. "
    "Please try again later or contact support at 1800‑123‑456."
)

# Point to service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex_credentials.json"

# Init Vertex AI
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")
LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-pro")
chat_session: ChatSession = model.start_chat()

def chat_completion(system_prompt, user_input, model_name="gemini-pro"):
    try:
        full_prompt = f"{system_prompt.strip()}\n\nUser: {user_input.strip()}\nAssistant:"
        response = chat_session.send_message(full_prompt)
        return response.text.strip()
    except Exception as e:
        print("[Gemini Vertex Error]", e)
        return FALLBACK_REPLY
