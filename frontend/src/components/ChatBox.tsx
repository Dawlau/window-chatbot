import React, { ChangeEvent, FormEvent, useEffect, useRef } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import ReactMarkdown from 'react-markdown';

interface Message {
    text: string;
    type: string;
}

interface ChatBoxProps {
    messages: Message[];
    fetchWelcomeMessage: (sessionId: string) => void;
    sessionId: string;
    handleSubmit: (event: FormEvent<HTMLFormElement>) => void;
    question: string;
    setQuestion: (value: string) => void;
}

const ChatBox: React.FC<ChatBoxProps> = ({ messages, fetchWelcomeMessage, sessionId, handleSubmit, question, setQuestion }) => {
    const chatBoxRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        fetchWelcomeMessage(sessionId);
    }, [fetchWelcomeMessage, sessionId]);

    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [messages]);

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setQuestion(e.target.value);
    };

    return (
        <Box className="App">
            <Typography variant="h4" component="h1" gutterBottom>
                Ask the Window Manufacturing Chatbot
            </Typography>
            <div id="chat-box" ref={chatBoxRef}>
                {messages.map((msg, index) => (
                    <Box key={index} className={`message ${msg.type}-message`}>
                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                    </Box>
                ))}
            </div>
            <form onSubmit={handleSubmit} id="chat-form">
                <TextField
                    fullWidth
                    value={question}
                    onChange={handleInputChange}
                    placeholder="Ask a question..."
                    id="question"
                    variant="outlined"
                    size="small"
                    style={{ marginRight: '10px', backgroundColor: '#333' }}
                    InputProps={{ style: { color: '#e0e0e0' } }}
                />
                <Button type="submit" variant="contained" color="primary">
                    Send
                </Button>
            </form>
        </Box>
    );
}

export default ChatBox;
