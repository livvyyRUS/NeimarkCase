from langchain_openai import ChatOpenAI

def get_llm(base_url: str, model_name: str, api_key: str):
    """
    Get a language model instance based on the provided base URL, model name, and API key.

    Args:
        base_url (str): The base URL of the language model API.
        model_name (str): The name of the language model to use.
        api_key (str): The API key for authentication.
    """
    
    llm = ChatOpenAI(
        base_url=base_url,
        model=model_name,
        api_key=api_key,
        temperature=0.05,
    )
    
    return llm