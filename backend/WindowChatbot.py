from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_groq import ChatGroq


class WindowChatbot:
    """
    A chatbot designed to answer questions about window manufacturing.
    
    Attributes:
        memory (ChatMessageHistory): The history of chat messages.
        prompt (ChatPromptTemplate): The chat prompt template.
        llm (ChatGroq): The language model used for generating responses.
        chain (Any): The pipeline combining the prompt and the language model.
        chain_with_memory (RunnableWithMessageHistory): The pipeline with memory integration.
    """

    def __init__(self, api_key: str, max_num_tokens: int) -> None:
        """
        Initializes the WindowChatbot with the provided API key.
        
        Args:
            api_key (str): The API key for the ChatGroq language model.
        """
        self.memory = ChatMessageHistory()
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a powerful assistant that specializes in answering questions regarding window manufacturing.
                    Provide detailed and accurate information without using any markdown in your responses. Always ensure clarity and precision.
                    If you don't know the answer, suggest checking external sources for the latest data.""",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        self.max_num_tokens = max_num_tokens

        self.llm = ChatGroq(api_key=api_key, max_tokens=self.max_num_tokens)
        self.chain = self.prompt | self.llm

        self.chain_with_memory = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def ask(self, question: str, session_id: str) -> str:
        """
        Asks a question to the chatbot and returns the response.
        
        Args:
            question (str): The question to ask the chatbot.
        
        Returns:
            str: The response from the chatbot.
        """
        response = self.chain_with_memory.invoke(
            {"input": question}, 
            {"configurable": {"session_id": session_id}}
        )
        return response.content
