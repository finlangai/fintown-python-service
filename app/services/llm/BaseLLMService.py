import os, time
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
        """Invoke the LLM with retry logic in case of rate limit"""
        for attempt in range(MAX_RETRIES):
            try:
                return self.llm.invoke(prompt).content
            except (
                Exception
            ) as e:  # Replace Exception with the specific exception for rate limit if known
                print(f"Attempt {attempt + 1}/{MAX_RETRIES} failed with error: {e}")
                if attempt < MAX_RETRIES - 1:
                    print("Retrying in 60 seconds...")
                    time.sleep(60)  # Wait for 60 seconds before retrying
                else:
                    print("Max retries reached. Exiting.")
                    raise
