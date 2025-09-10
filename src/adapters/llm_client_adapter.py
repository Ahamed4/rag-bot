from typing import Any

class LLMClientAdapter:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def invoke(self, prompt: str, **kwargs) -> Any:
        # Try to call the client's invoke method with the prompt
        try:
            # For clients that expect 'input' or 'prompt'
            return self.llm_client.invoke(prompt, **kwargs)
        except TypeError:
            # For clients that expect 'input' as a named argument
            return self.llm_client.invoke(input=prompt, **kwargs)