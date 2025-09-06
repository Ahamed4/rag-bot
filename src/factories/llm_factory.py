from llm_providers.base import LLMProvider
from llm_providers.openai_llm import OpenAIChatLLM
from llm_providers.google_llm import GoogleChatLLM
from llm_providers.ollama_llm import OllamaChatLLM
from llm_providers.groq_llm import GroqChatLLM

class LLMFactory:
    _providers = {
            "openai": OpenAIChatLLM(),
            "ollama": OllamaChatLLM(),
            "google": GoogleChatLLM(),
            "groq": GroqChatLLM(),
            # Future providers can be added here
        }
    @staticmethod
    def get_llm_provider(provider_name: str) -> LLMProvider:
        provider = LLMFactory._providers.get(provider_name.lower())

        if not provider:
            raise ValueError(f"Provider '{provider_name}' not supported. Available providers: {', '.join(LLMFactory._providers.keys())}")
        
        return provider
    @staticmethod
    def get_supported_providers() -> list:
        return list(LLMFactory._providers.keys())