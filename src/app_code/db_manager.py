import chromadb
from paths import VECTOR_DB_DIR
from app_code.logger import logger

_client = None

def get_client():
    """Get or create a ChromaDB client singleton."""
    global _client
    if _client is None:
        logger.debug(f"Initializing ChromaDB client at {VECTOR_DB_DIR}")
        _client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    return _client

def get_collection(collection_name="publications"):
    """Get a collection from the client."""
    client = get_client()
    try:
        return client.get_collection(name=collection_name)
    except Exception:
        logger.warning(f"Collection {collection_name} not found")
        return None

def shutdown():
    """Properly shutdown the ChromaDB client."""
    global _client
    if _client is not None:
        _client = None
        
        # Force garbage collection
        import gc
        gc.collect()
        logger.debug("ChromaDB client shut down successfully")