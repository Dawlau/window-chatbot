from flask import Flask, request, jsonify
from flask_cors import CORS
from WindowChatbot import WindowChatbot
import os


app = Flask(__name__)
CORS(app)

app.config["CORS_ORIGINS"] = os.getenv("CORS_ORIGINS")

API_KEY = os.getenv("GROQ_API_KEY")
chatbot = WindowChatbot(api_key=API_KEY)


@app.route("/api/chat", methods=["POST"])
async def chat():
    data = request.get_json()
    question = data.get("question")

    if question:
        response = chatbot.ask(question)
        return jsonify({"response": response})

    return jsonify({"error": "No question provided"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
