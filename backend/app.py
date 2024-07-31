from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import ConversationChain
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('GROQ_API_KEY')
chatbot = ConversationChain(llm=Groq(API_KEY))

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')
    if question:
        response = chatbot.run(question)
        return jsonify({'response': response})
    return jsonify({'error': 'No question provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
