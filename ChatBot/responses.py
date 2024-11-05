# responses.py
from casualResponse import handle_casual_response
from upload import search_wikipedia
from fuzzywuzzy import fuzz
from faqData import faqs

def get_chat_response(user_input):
    user_input_lower = user_input.lower().strip()

    # Define the MAIN MENU button HTML
    main_menu_button = "<button onclick=\"sendMessage('MAIN MENU')\">MAIN MENU</button>"

    faq_response = handle_faq(user_input)
    if faq_response:
        return faq_response

    if user_input_lower == "main menu":
        user_input_lower = "initial_greeting"  # Redirect to the "existing customer" response

    # Step 1: Handle specific button-based interactions
    if user_input_lower == "initial_greeting":
        return """
            Hi, welcome to CEX!<br>
            Are you a New customer or Existing customer?<br>
            <button onclick="sendMessage('New customer')">New Customer</button>
            <button onclick="sendMessage('Existing customer')">Existing Customer</button>
        """

    if user_input_lower == "existing customer":
        return f"""
            Hi, what would you like to do?<br>
            <button onclick="sendMessage('BUY')">BUY</button>
            <button onclick="sendMessage('SELL')">SELL</button>
            <button onclick="sendMessage('EXCHANGE')">EXCHANGE</button><br>{main_menu_button}
        """

    if user_input_lower == "new customer":
        return "Welcome! How can I assist you with getting started at CeX?"

    if user_input_lower == "buy":
        return f"""
            What would you like to Buy from CeX?<br>
            <button onclick="sendMessage('PHONES')">PHONES</button>
            <button onclick="sendMessage('COMPUTING')">COMPUTING</button>
            <button onclick="sendMessage('CONSOLE GAMING')">CONSOLE GAMING</button><br>{main_menu_button}
        """

    if user_input_lower == "phones":
        return f"""
            Please choose a category:<br>
            <button onclick="sendMessage('SMART PHONE')">SMART PHONE</button>
            <button onclick="sendMessage('FEATURED PHONES')">FEATURED PHONES</button><br>{main_menu_button}
        """

    if user_input_lower == "smart phone":
        return f"""
            Click the links below to visit categories from CeX:<br>
            Click <a href="https://uk.webuy.com/search?categoryIds=979&categoryName=Phones%20Android" target="_blank">here</a> to visit Android phones from CeX!<br>
            Click <a href="https://uk.webuy.com/search?categoryIds=844&categoryName=Phones%20iPhone" target="_blank">here</a> to visit iPhone from CeX!<br>
            Click <a href="https://uk.webuy.com/search?categoryIds=989&categoryName=Phones%20Windows%20Phone" target="_blank">here</a> to visit Windows Phone from CeX!<br>{main_menu_button}
        """

        # Step 2: Check for casual responses
    casual_response = handle_casual_response(user_input)
    if casual_response:
        return f"{casual_response}<br>{main_menu_button}"

    # Step 3: Use Wikipedia for out-of-scope/general questions
    wiki_response = search_wikipedia(user_input)
    if wiki_response:
        return f"{wiki_response}<br>Please ask something related to CeX. Visit our CeX website by clicking <br>{main_menu_button}"

    # Default response if input is unrecognized
    return f"I'm not sure how to respond to that. Please choose an option or ask a question.<br>{main_menu_button}"

def handle_faq(user_input):
    main_menu_button = "<button onclick=\"sendMessage('MAIN MENU')\">MAIN MENU</button>"
    for question, answer in faqs.items():
        if fuzz.ratio(user_input.lower(), question) > 80:  # 80% similarity threshold
            return f"{answer}<br>{main_menu_button}"  # Append the main menu button to the answer
    return None  # If no match is found, return None
