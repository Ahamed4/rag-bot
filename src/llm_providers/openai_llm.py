from dataclasses import dataclass,field
from typing import Optional
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from adapters.llm_client_adapter import LLMClientAdapter
from app_code.utils import load_env
import os

@dataclass
class OpenAIChatLLM:
    api_key: Optional[str] = field(init=False)
    default_model_name: str = "gpt-3.5-turbo"

    def __post_init__(self):
        load_env()
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def create_llm(self, model_name=None, temperature=0.0, **kwargs) -> LLMClientAdapter:
        model_name = model_name or self.default_model_name

        if self.api_key is None:
            raise ValueError("OpenAI API key is missing. Please set the API key.")

        client = ChatOpenAI(
            api_key=SecretStr(self.api_key),
            model=model_name,
            temperature=temperature,
            **kwargs
        )

        return LLMClientAdapter(client)