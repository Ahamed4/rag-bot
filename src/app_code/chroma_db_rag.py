import os
import logging
from adapters.llm_client_adapter import LLMClientAdapter
from app_code.utils import load_yaml_config
from app_code.prompt_builder import build_prompt_from_config
from app_code.chroma_db_ingest import get_db_collection, embed_documents
from app_code.initialize_llm import main as initialize_llm
from app_code.logger import logger
from app_code.db_manager import get_collection
from paths import APP_CONFIG_FPATH, PROMPT_CONFIG_FPATH, OUTPUTS_DIR

# To avoid tokenizer parallelism warning from huggingface
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# collection = get_db_collection(collection_name="publications")
collection = get_collection(collection_name="publications")

def retrieve_relevant_documents(
    query: str,
    n_results: int = 5,
    threshold: float = 0.3,
) -> list[str]:
    """
    Query the ChromaDB database with a string query.

    Args:
        query (str): The search query string
        n_results (int): Number of results to return (default: 5)
        threshold (float): Threshold for the cosine similarity score (default: 0.3)

    Returns:
        dict: Query results containing ids, documents, distances, and metadata
    """
    logger.debug(f"Retrieving relevant documents for query: {query}")
    relevant_results = {
        "ids": [],
        "documents": [],
        "distances": [],
    }
    # Embed the query using the same model used for documents
    logger.debug("Embedding query...")
    query_embedding = embed_documents([query])[0]  # Get the first (and only) embedding

    logger.info("Querying collection...")
    # Query the collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "distances"],
    )

    if (
        results is None or
        results.get("ids") is None or
        results.get("documents") is None or
        results.get("distances") is None or
        not results["ids"] or
        not results["documents"] or
        not results["distances"]
    ):
        logger.warning("No results found.")
        return []

    logger.debug("Filtering results...")
    keep_item = [False] * len(results["ids"][0])
    for i, distance in enumerate(results["distances"][0]):
        if distance < threshold:
            keep_item[i] = True

    for i, keep in enumerate(keep_item):
        if keep:
            relevant_results["ids"].append(results["ids"][0][i])
            relevant_results["documents"].append(results["documents"][0][i])
            relevant_results["distances"].append(results["distances"][0][i])

    return relevant_results["documents"]

def respond_to_query(
    prompt_config: dict,
    query: str,
    llm: LLMClientAdapter,
    n_results: int = 5,
    threshold: float = 0.3,
) -> str:
    """
    Respond to a query using the ChromaDB database.
    """

    relevant_documents = retrieve_relevant_documents(
        query, n_results=n_results, threshold=threshold
    )

    logger.debug("-" * 100)
    logger.debug("Relevant documents: \n")
    for doc in relevant_documents:
        logger.debug(doc)
        logger.debug("-" * 100)
    logger.debug("")

    logger.debug("User's question:")
    logger.debug(query)
    logger.debug("")
    logger.debug("-" * 100)
    logger.debug("")
    input_data = (
        f"Relevant documents:\n\n{relevant_documents}\n\nUser's question:\n\n{query}"
    )

    rag_assistant_prompt = build_prompt_from_config(
        prompt_config, input_data=input_data
    )

    logger.debug(f"RAG assistant prompt: {rag_assistant_prompt}")
    logger.debug("")

    response = llm.invoke(rag_assistant_prompt)
    return response.content

def main():
    app_config = load_yaml_config(APP_CONFIG_FPATH)
    prompt_config = load_yaml_config(PROMPT_CONFIG_FPATH)

    rag_assistant_prompt = prompt_config["rag_assistant_prompt"]
    vectordb_params = app_config["vectordb"]
    llm_client = initialize_llm()

    exit_app = False
    while not exit_app:
        query = input(
            "Enter a question, 'config' to change the parameters, 'llm' to change the LLM, or 'exit' to quit: "
        )
        if query == "exit":
            exit_app = True
            exit()

        elif query == "config":
            threshold = float(input("Enter the retrieval threshold: "))
            n_results = int(input("Enter the Top K value: "))
            vectordb_params = {
                "threshold": threshold,
                "n_results": n_results,
            }
            continue
        elif query == "llm":
            llm_client = initialize_llm()
            continue

        response = respond_to_query(
            prompt_config=rag_assistant_prompt,
            query=query,
            llm=llm_client,
            **vectordb_params,
        )
        logger.info("-" * 100)
        logger.info("LLM response:")
        logger.info(response + "\n\n")

if __name__ == "__main__":
    main()

