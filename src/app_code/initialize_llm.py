import os
from factories.llm_factory import LLMFactory
from app_code.utils import load_yaml_config
from paths import APP_CONFIG_FPATH, OUTPUTS_DIR
import logging

logger = logging.getLogger()

def setup_logging():

    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(os.path.join(OUTPUTS_DIR, "rag_assistant.log"))
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_provider_choice():
    providers = LLMFactory.get_supported_providers()
    print("Supported LLM Providers:")
    for idx, name in enumerate(providers, 1):
        print(f"{idx}. {name.capitalize()}")
    choice = input(f"Choose provider [default: groq]: ").strip()
    if not choice:
        return "groq"
    try:
        idx = int(choice)
        if 1 <= idx <= len(providers):
            return providers[idx-1]
    except ValueError:
        if choice in providers:
            return choice
    print("Invalid choice, please try again.")
    return get_provider_choice()

def get_llm_parameters(provider_name):
    app_config = load_yaml_config(APP_CONFIG_FPATH)
    default_models = app_config.get("default_llm_models", {})
    model_name = default_models.get(provider_name)
    model_name = input(f"Enter model name for '{provider_name.capitalize()}' llm [default: {model_name}]: ").strip() or model_name
    temperature = input("Enter temperature [default: 0.0]: ").strip()
    temperature = float(temperature) if temperature else 0.0
    return model_name, temperature

def main():
    setup_logging()
    logging.info("-" * 100)
    print("Welcome to the Interactive LLM Terminal!")
    provider_name = get_provider_choice()
    print(f"Selected provider: {provider_name}")
    model_name, temperature = get_llm_parameters(provider_name)
    try:
        llm_provider = LLMFactory.get_llm_provider(provider_name)
        llm = llm_provider.create_llm(model_name=model_name, temperature=temperature)
        print(f"Success! Instantiated '{provider_name.capitalize()}' LLM with model '{model_name}' and temperature {temperature}.")
    except Exception as e:
        print(f"Error instantiating LLM: {e}")
        return

    while True:
        question = input("\nEnter your question (or 'q' to quit): ").strip()
        if question.lower() == 'q':
            print("Goodbye!")
            break
        try:
            if llm is None:
                raise RuntimeError("LLM creation failed. Check your configuration and API keys.")
            response = llm.invoke(question)
            print(f"Answer:\n{getattr(response, 'content', response)}")
            logging.info("-" * 100)
            logging.info("LLM response:")
            logging.info(response + "\n\n")
        except Exception as e:
            print(f"Error invoking LLM: {e}")
        

if __name__ == "__main__":
    main()
    

