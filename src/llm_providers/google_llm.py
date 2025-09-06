from dataclasses import dataclass, field
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from code.utils import load_env
import os

@dataclass
class GoogleChatLLM:
    api_key: Optional[str] = field(init=False)
    default_model_name: str = "gemini-2.5-flash"

    def __post_init__(self):
        load_env()
        self.api_key = os.getenv("GOOGLE_API_KEY")
    
    def create_llm(self, model_name=None, temperature = 0.0, **kwargs):
        
        model_name = model_name or self.default_model_name

        if self.api_key is None:
            raise ValueError("Gemini API key is missing. Please set the API key.")

        return ChatGoogleGenerativeAI(
            api_key=self.api_key, 
            model=model_name, 
            temperature=temperature, 
            **kwargs
        )


       