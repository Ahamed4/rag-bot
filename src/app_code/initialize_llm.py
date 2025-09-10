import os
from adapters.llm_client_adapter import LLMClientAdapter
from factories.llm_factory import LLMFactory
from app_code.utils import load_yaml_config
from paths import APP_CONFIG_FPATH, OUTPUTS_DIR
from app_code.logger import logger

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
    
def main() -> LLMClientAdapter | None:
    logger.info("Let us initialize the LLM.")
    provider_name = get_provider_choice()
    logger.info(f"Selected provider: {provider_name}")
    model_name, temperature = get_llm_parameters(provider_name)
    try:
        llm_provider = LLMFactory.get_llm_provider(provider_name)
        llm = llm_provider.create_llm(model_name=model_name, temperature=temperature)
        logger.info(f"Success! Instantiated '{provider_name.capitalize()}' LLM with model '{model_name}' and temperature {temperature}.")
        return llm
    except Exception as e:
        logger.error(f"Error instantiating LLM: {e}")
        return        

if __name__ == "__main__":
    main()
    

