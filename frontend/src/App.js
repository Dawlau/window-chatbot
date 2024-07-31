import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [question, setQuestion] = useState('');
    const [messages, setMessages] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (question.trim() === '') return;

        const userMessage = { type: 'user', text: question };
        setMessages([...messages, userMessage]);
        setQuestion('');

        try {
            const res = await axios.post(process.env.REACT_APP_CHAT_API_URL, { question });
            const botMessage = { type: 'bot', text: res.data.response };
            setMessages(prevMessages => [...prevMessages, botMessage]);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h1>Ask the Window Manufacturing Chatbot</h1>
            <div id="chat-box">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.type}-message`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit} id="chat-form">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question..."
                    id="question"
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
}

export default App;
