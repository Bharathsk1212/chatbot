from flask import Flask, render_template, request, jsonify
from responses import get_chat_response  # Import the function from responses.py
from upload import classify_image, search_wikipedia  # Separate image classification functions
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)


# Route for the main chat page
@app.route("/")
def index():
    return render_template('chat.html')


# Chatbot response route
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg", "").strip()  # Safely retrieve and strip the message from the form

    # Check if this is the initial request with no user input
    if not msg:
        # Initial greeting message with buttons for New or Existing customer
        initial_message = """
                Hi, welcome to CEX!<br>
                Are you a New customer or Existing customer?<br>
                <button onclick="sendMessage('New customer')">New Customer</button>
                <button onclick="sendMessage('Existing customer')">Existing Customer</button>
            """
        return initial_message
    try:
        response = get_chat_response(msg)  # Get the chat response from the function
        return response
    except Exception as e:
        logging.error(f"Error in chat: {str(e)}")
        return f"An error occurred: {str(e)}"


# Image upload route for classification and search
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Get the image from the request
        file = request.files['image']

        # Classify the uploaded image
        classified_label = classify_image(file)

        # Perform a web search using the classified label
        search_result = search_wikipedia(classified_label)

        # Return the classification result and search data
        return jsonify({
            'label': classified_label,
            'search_result': search_result
        })

    except Exception as e:
        logging.error(f"Error in image upload: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
