from dataclasses import dataclass
from langchain_community.chat_models import ChatOllama
from adapters.llm_client_adapter import LLMClientAdapter


@dataclass
class OllamaChatLLM:
    default_model_name: str = "llama3-8b-8192"
    
    def create_llm(self, model_name=None, temperature = 0.0, **kwargs) -> LLMClientAdapter:
        
        model_name = model_name or self.default_model_name

        client = ChatOllama(
            model=model_name, 
            temperature=temperature, 
            **kwargs
        )

        return LLMClientAdapter(client)