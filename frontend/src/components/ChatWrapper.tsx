import React, { useState, FormEvent, ChangeEvent, useEffect } from 'react';
import ChatBox from "./ChatBox";
import axios from "axios";

interface Message {
    type: string;
    text: string;
}

const ChatWrapper: React.FC = () => {
    const [question, setQuestion] = useState<string>('');
    const [sessionId, setSessionId] = useState<string>('');
    const [messages, setMessages] = useState<Message[]>([]);

    const loginUser = async () => {
        try {
            const res = await axios.post(`${process.env.REACT_APP_API_URL}/api/login`, {}, { withCredentials: true });
            setSessionId(res.data.session_id);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    useEffect(() => {
        loginUser();
    }, []);

    const fetchWelcomeMessage = async (sessionId: string) => {

        try {
            const res = await axios.post(`${process.env.REACT_APP_API_URL}/api/chat`, { question: 'Hello', session_id: sessionId }, { withCredentials: true });
            const botMessage: Message = { type: 'bot', text: res.data.response };
            setMessages([botMessage]);
        } catch (error) {
            console.error('Error fetching welcome message:', error);
        }
    };

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (question.trim() === '') return;

        const userMessage: Message = { type: 'user', text: question };
        setMessages([...messages, userMessage]);
        setQuestion('');

        try {
            const res = await axios.post(`${process.env.REACT_APP_API_URL}/api/chat` as string, { question: question, session_id: sessionId }, { withCredentials: true });
            const botMessage: Message = { type: 'bot', text: res.data.response };
            setMessages(prevMessages => [...prevMessages, botMessage]);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        sessionId ?
            <ChatBox messages={messages} fetchWelcomeMessage={fetchWelcomeMessage} sessionId={sessionId} handleSubmit={handleSubmit} question={question} setQuestion={setQuestion} />
            :
            <></>
    );
};

export default ChatWrapper;
