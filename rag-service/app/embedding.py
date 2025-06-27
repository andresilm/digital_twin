from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

CHUNKS_SIZE = 500
CHUNKS_OVERLAP = int(CHUNKS_SIZE * 0.1)


def split_to_chunks(full_profile: str):
    """
    Splits a large text profile into smaller chunks for embedding or retrieval.

    Args:
        full_profile (str): The full text content of the profile to split.

    Returns:
        List[Document]: A list of LangChain Document objects, each containing
                        a chunk of the original text with metadata indicating the source.

    Behavior:
        - Wraps the full_profile text inside a single Document with metadata.
        - Uses RecursiveCharacterTextSplitter to split the Document into chunks,
          with chunks of size 300 characters and an overlap of 50 characters.
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

    Behavior:
        - Logs info messages when loading starts and finishes.
        - Uses the "BAAI/bge-small-en-v1.5" model for embeddings.
    """
    logger.debug('Loading Embedding')
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    logger.debug('Done')
    return embeddings
