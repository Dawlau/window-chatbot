from flask import Flask, request, jsonify
from flask_cors import CORS
from WindowChatbot import WindowChatbot
from typing import Any, Dict, Union
import os

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Set CORS origins from environment variable
app.config["CORS_ORIGINS"] = os.getenv("CORS_ORIGINS")

API_KEY = os.getenv("GROQ_API_KEY")
chatbot = WindowChatbot(api_key=API_KEY)


@app.route("/api/health", methods=["GET"])
def health() -> Dict[str, str]:
    """
    Endpoint to check the health of the API.

    Returns:
        JSON response containing the status of the API.
    """
    return jsonify({"status": "healthy"})


@app.route("/api/chat", methods=["POST"])
async def chat() -> Union[Dict[str, Any], tuple[Dict[str, str], int]]:
    """
    Endpoint to handle chat requests. Expects a JSON payload with a "question" field.

    Returns:
        JSON response containing the chatbot's answer or an error message.
    """
    data = request.get_json()
    question = data.get("question")

    if question:
        response = chatbot.ask(question)
        return jsonify({"response": response})

    return jsonify({"error": "No question provided"}), 400


if __name__ == "__main__":
    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)
