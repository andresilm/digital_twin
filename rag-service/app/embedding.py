from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

CHUNKS_SIZE = 500
CHUNKS_OVERLAP = int(CHUNKS_SIZE * 0.1)
EMBEDDING_MODEL = "BAAI/bge-m3"


def split_to_chunks(full_profile: str):
    """
    Splits a large text profile into smaller chunks for embedding or retrieval.

    Args:
        full_profile (str): The full text content of the profile to split.

    Returns:
        List[Document]: A list of LangChain Document objects, each containing
                        a chunk of the original text with metadata indicating the source.
    """
    docs = [
        Document(page_content=full_profile, metadata={"source": "profile_json"}),
    ]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNKS_SIZE, chunk_overlap=CHUNKS_OVERLAP)
    docs_split = text_splitter.split_documents(docs)
    return docs_split


def load_embeddings():
    """
    Loads a HuggingFace embedding model to convert text chunks into vector embeddings.

    Returns:
        HuggingFaceEmbeddings: An instance of the embedding model loaded.
    """
    logger.debug('Loading Embedding')
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    logger.debug('Done')
    return embeddings
