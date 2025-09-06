from typing import Protocol

class LLMProvider(Protocol):
    def create_llm(self, **kwargs):
        """Create and return a client instance for the LLM provider."""
        pass