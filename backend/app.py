from flask import Flask, request, jsonify, session
from flask_cors import CORS
from WindowChatbot import WindowChatbot
from typing import Any, Dict, Union
import os
import uuid

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, supports_credentials=True)

# Set CORS origins from environment variable
app.config["CORS_ORIGINS"] = os.getenv("CORS_ORIGINS")
app.secret_key = os.getenv("SECRET_KEY")

API_KEY = os.getenv("GROQ_API_KEY")
MAX_NUM_TOKENS = 500

chatbot = WindowChatbot(api_key=API_KEY, max_num_tokens=MAX_NUM_TOKENS)


@app.route("/api/health", methods=["GET"])
async def health() -> Dict[str, str]:
    """
    Endpoint to check the health of the API.

    Returns:
        JSON response containing the status of the API.
    """
    return jsonify({"status": "healthy"})


@app.route("/api/login", methods=["POST"])
async def login() -> Dict[str, str]:
    """
    Endpoint to generate a session id for the user.

    Returns:
        JSON response containing the login status.
    """
    session["session_id"] = str(uuid.uuid4())
    return jsonify({"session_id": session["session_id"]})


@app.route("/api/chat", methods=["POST"])
async def chat() -> Union[Dict[str, Any], tuple[Dict[str, str], int]]:
    """
    Endpoint to handle chat requests. Expects a JSON payload with a "question" field.

    Returns:
        JSON response containing the chatbot's answer or an error message.
    """
    if "session_id" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    question = data.get("question")
    session_id = data.get("session_id")

    if session_id is None:
        return jsonify({"error": "User not logged in"}), 401
    
    if session_id != session["session_id"]:
        return jsonify({"error": "Invalid session id"}), 401
    
    if question:
        response = chatbot.ask(question, session_id)
        return jsonify({"response": response})

    return jsonify({"error": "No question provided"}), 400


if __name__ == "__main__":
    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)
