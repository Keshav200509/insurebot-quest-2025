

# from engine.memory import MemoryBuffer
# from engine.state import ConversationState
# from engine.planner import load_customer, personalize, build_prompt
# # from models.retriever import retrieve_facts
# from models.retriever import  retrieve_facts
# from models.gpt import chat_completion
# import os
# import json
# from datetime import datetime
# from engine.objection_loop import ObjectionManager


# def log_session(log_data):
#     os.makedirs("logs", exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     log_path = f"logs/session_{timestamp}.json"
#     with open(log_path, "w") as f:
#         json.dump(log_data, f, indent=2)

# def run_bot(customer_id="customer123"):
#     customer = load_customer(customer_id)
#     state = ConversationState(customer)
#     memory = MemoryBuffer()
#     session_log = []
#     objection_mgr = ObjectionManager()  # ← Moved up here

#     print()
#     while state.is_active():
#         user_input = input("👤 You: ").strip()
#         if not user_input:
#             continue

#         session_log.append({"user": user_input})

#         # FSM decides response or triggers GPT
#         bot_reply = state.next(user_input)

#         if bot_reply is not None:
#             bot_reply = personalize(bot_reply, customer)
#             print("🤖 InsureBot:", bot_reply)
#             session_log[-1]["bot"] = bot_reply
#             memory.add_turn(user_input, bot_reply)
#             continue

#         # NEW: Handle objection instead of going straight to GPT
#         if state.state == "handle_objection":
#             reply = objection_mgr.handle(user_input, customer)
#             print("🤖 InsureBot:", reply)
#             memory.add_turn(user_input, reply)
#             session_log.append({"user": user_input, "bot": reply})
#             continue

#         # Fallback: GPT + RAG
#         kb_chunks = retrieve_facts(user_input)
#         memory_text = memory.get_recent_context()
#         prompt = build_prompt(user_input, kb_chunks, memory_text, state.state, customer)

#         reply = chat_completion(prompt, user_input)
#         reply = personalize(reply, customer)

#         print("🤖 InsureBot:", reply)
#         session_log[-1]["bot"] = reply
#         memory.add_turn(user_input, reply)

#     print("🤖 InsureBot: Goodbye!\n")
#     session_log.append({"bot": "Goodbye!"})
#     log_session(session_log)


# if __name__ == "__main__":
#     run_bot()


# ======================================================
# FILE: main.py
# PURPOSE: Entry point - GPT-led insurance assistant loop
# ======================================================

# ======================================
# main.py — Gemini-powered conversation
# ======================================

# from models.gpt import chat_completion
# from models.retriever import retrieve_facts
# from memory.buffer import MemoryBuffer
# from engine.customer_loader import load_customer
# from engine.prompt_builder import build_prompt
# from utils.emotion import analyze_sentiment
# from datetime import datetime
# import json, os

# def log_session(session):
#     os.makedirs("logs", exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     with open(f"logs/session_{timestamp}.json", "w") as f:
#         json.dump(session, f, indent=2)

# def run_bot(customer_id="customer123"):
#     customer = load_customer(customer_id)
#     memory = MemoryBuffer()
#     session_log = []

#     print(f"\n🤖 InsureBot: Hello, this is Veena from ValuEnable. May I speak with {customer.get('name', 'you')}?")

#     while True:
#         user_input = input("👤 You: ").strip()
#         if not user_input:
#             continue

#         sentiment = analyze_sentiment(user_input)
#         kb_chunks = retrieve_facts(user_input)
#         memory_context = memory.get_recent_context()

#         prompt = build_prompt(
#             customer=customer,
#             memory=memory_context,
#             kb_chunks=kb_chunks,
#             user_input=user_input,
#             tone=sentiment
#         )

#         reply = chat_completion(prompt, user_input)
#         print("🤖 InsureBot:", reply)

#         memory.add_turn(user_input, reply)
#         session_log.append({"user": user_input, "bot": reply})

#         if any(word in user_input.lower() for word in ["bye", "goodbye", "not interested"]):
#             break

#     print("🤖 InsureBot: Thank you, take care!\n")
#     log_session(session_log)

# if __name__ == "__main__":
#     run_bot()

# main.py

# main.py

from engine.fsm import ConversationFSM
from engine.customer_loader import load_customer
from engine.prompt_builder import personalize, build_prompt
from engine.objection_loop import ObjectionHandler
from models.retriever import retrieve_facts
from models.gpt import chat_completion
from datetime import datetime
import os
import json

# ----------------------------------------
# Simple session memory without extra file
# ----------------------------------------
class ConversationMemory:
    def __init__(self, max_turns=5):
        self.turns = []
        self.max_turns = max_turns

    def add(self, user_input, bot_reply):
        self.turns.append((user_input, bot_reply))
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)

    def get_memory_text(self):
        return "\n".join([f"User: {u}\nBot: {b}" for u, b in self.turns])

# ----------------------------------------
# Logging function
# ----------------------------------------
def log_session(log_data):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"logs/session_{timestamp}.json", "w") as f:
        json.dump(log_data, f, indent=2)

# ----------------------------------------
# Run the bot
# ----------------------------------------
def run_bot(customer_id="customer123"):
    customer = load_customer(customer_id)
    fsm = ConversationFSM(customer)
    memory = ConversationMemory()
    objections = ObjectionHandler()
    session_log = []

    print()  # space

    # Start conversation with FSM
    bot_msg = fsm.next("")  # empty input to trigger greeting
    print("🤖 InsureBot:", bot_msg)
    session_log.append({"bot": bot_msg})

    while fsm.is_active():
        user_input = input("👤 You: ").strip()
        if not user_input:
            continue

        session_log.append({"user": user_input})

        # FSM handles simple paths
        bot_msg = fsm.next(user_input)
        if bot_msg:
            print("🤖 InsureBot:", bot_msg)
            session_log[-1]["bot"] = bot_msg
            memory.add(user_input, bot_msg)
            continue

        # Objection handling
        if fsm.state == "post_objection":
            reply = objections.handle(user_input, customer)
            print("🤖 InsureBot:", reply)
            memory.add(user_input, reply)
            session_log[-1]["bot"] = reply
            break  # End after handling objection

        # Fallback to GPT/Gemini using prompt
        kb_chunks = retrieve_facts(user_input)
        history = memory.get_memory_text()
        tone = "neutral"  # fixed tone for now
        prompt = build_prompt(customer, history, kb_chunks, user_input, tone)

        reply = chat_completion(prompt, user_input)
        print("🤖 InsureBot:", reply)
        memory.add(user_input, reply)
        session_log[-1]["bot"] = reply

    print("🤖 InsureBot: Goodbye!")
    session_log.append({"bot": "Goodbye!"})
    log_session(session_log)


if __name__ == "__main__":
    run_bot()
