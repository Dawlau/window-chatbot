from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_groq import ChatGroq
from uuid import uuid4


class WindowChatbot:
    def __init__(self, api_key):
        self.memory = ChatMessageHistory()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a powerful assistant that specializes in answering questions regarding window manufacturing. 
                    Make sure to not include any markdown in your responses""",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        self.llm = ChatGroq(api_key=api_key)

        self.chain = self.prompt | self.llm

        self.chain_with_memory = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def ask(self, question):
        response = self.chain_with_memory.invoke(
            {"input": question}, 
            {"configurable": {"session_id": "unused"}}
        )
        return response.content