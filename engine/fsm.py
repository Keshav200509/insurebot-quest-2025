# engine/fsm.py

class ConversationFSM:
    def __init__(self, customer):
        self.customer = customer
        self.state = "greeting"
        self.objection = None

    def next(self, user_input):
        text = user_input.strip().lower()

        if self.state == "greeting":
            self.state = "verify_identity"
            return "Hello, this is Veena from ValuEnable. May I speak with [name]?"

        if self.state == "verify_identity":
            if any(word in text for word in ["yes", "speaking", "this is"]):
                self.state = "premium_due"
                return "Your premium of ₹[premium_amount] is due on [due_date]. Would you like to pay now?"
            return "I'm sorry, could you confirm again if I'm speaking with [name]?"

        if self.state == "premium_due":
            if "yes" in text:
                self.state = "confirm_payment"
                return "That’s great! You can pay via [payment_mode]. Do you need help with that?"
            elif "no" in text:
                self.state = "handle_objection"
                return "Could you please share your reason for not paying the premium yet?"
            return "Could you clarify if you're able to pay the premium today?"

        if self.state == "confirm_payment":
            self.state = "end"
            return "Thank you for continuing your policy with us, [name]!"

        if self.state == "handle_objection":
            self.state = "post_objection"
            return None  # let Gemini handle

        return None  # fallback to Gemini

    def is_active(self):
        return self.state != "end"
