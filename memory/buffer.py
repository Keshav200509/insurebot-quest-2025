class MemoryBuffer:
    def __init__(self, max_turns=6):
        self.turns = []
        self.max_turns = max_turns

    def add_turn(self, user_input, bot_reply):
        self.turns.append({"user": user_input, "bot": bot_reply})
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)

    def get_recent_context(self):
        return "\n".join(
            f"User: {t['user']}\nBot: {t['bot']}" for t in self.turns
        )
