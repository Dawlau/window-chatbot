import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [question, setQuestion] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post(process.env.CHAT_API_URL, { question });
            setResponse(res.data.response);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h1>Ask the Window Manufacturing Chatbot</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question..."
                />
                <button type="submit">Send</button>
            </form>
            <div>
                <p>{response}</p>
            </div>
        </div>
    );
}

export default App;
