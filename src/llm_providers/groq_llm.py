from dataclasses import dataclass, field
from typing import Optional
from langchain_groq import ChatGroq
from pydantic import SecretStr
from app_code.utils import load_env
import os


@dataclass
class GroqChatLLM:
    api_key: Optional[str] = field(init=False)
    default_model_name: str = "llama-3.1-8b-instant"

    def __post_init__(self):
        load_env()
        self.api_key = os.getenv("GROQ_API_KEY")

    def create_llm(self, model_name=None, temperature = 0.0, **kwargs):   
        """ Use model_name from parameter or default if not provided."""
        model_name = model_name or self.default_model_name

        if self.api_key is None:
            raise ValueError("Groq API key is missing. Please set the API key.")
    
        return ChatGroq(
            api_key=SecretStr(self.api_key),
            model=model_name, 
            temperature=temperature, 
            **kwargs
        )