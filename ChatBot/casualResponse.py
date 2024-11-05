def handle_casual_response(user_input):
    user_input = user_input.lower().strip()

    # Simple keyword-based detection
    greetings = ["hi", "hello", "hey"]
    inquiries = ["how are you", "how's it going", "what's up"]
    identity = ["who are you", "what is your name", "tell me about yourself"]

    # Respond to greetings
    if any(greet in user_input for greet in greetings):
        return "Hello! How can I help you today?"

    # Respond to inquiries
    if any(inquiry in user_input for inquiry in inquiries):
        return "I'm doing great, thank you! How can I assist you today?"

    # Respond to identity questions
    if any(id_question in user_input for id_question in identity):
        return "I am the CeX Assistant, here to help you with buying, selling, and exchanging items at CeX."

    # If no casual match, return None
    return None
