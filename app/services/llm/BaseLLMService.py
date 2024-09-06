import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from config.llm import MODEL_NAME

# LOAD ENVIRONMENT VARIABLES
load_dotenv()


class BaseLLMService:
    def __init__(self) -> None:
        self.llm = ChatGroq(
            model=MODEL_NAME,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def invoke(self, prompt: str):
        """
        Invoke the LLM
        """
        return self.llm.invoke(prompt).content
