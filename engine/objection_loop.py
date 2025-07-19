# engine/objection_loop.py

from models.retriever import retrieve_facts
from models.gpt import chat_completion
from engine.prompt_builder import personalize, build_prompt


class ObjectionHandler:
    def __init__(self):
        pass

    def handle(self, user_input, customer):
        # Retrieve RAG info
        kb_chunks = retrieve_facts(user_input)
        memory_context = ""  # No full memory context needed in short objections
        state = "objection_resolution"

        prompt = build_prompt(
         customer,
         memory_context,
         kb_chunks,
         user_input,
         tone="concerned"
        )


        reply = chat_completion(prompt, user_input)
        return personalize(reply, customer)
