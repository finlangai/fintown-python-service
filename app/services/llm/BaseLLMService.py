import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from config.llm import MODEL_NAME, TEMPERATURE, MAX_TOKENS, TIMEOUT, MAX_RETRIES

# LOAD ENVIRONMENT VARIABLES
load_dotenv()


class BaseLLMService:
    def __init__(self) -> None:
        self.llm = ChatGroq(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            timeout=TIMEOUT,
            max_retries=MAX_RETRIES,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def invoke(self, prompt: str):
        """
        Invoke the LLM
        """
        return self.llm.invoke(prompt).content
