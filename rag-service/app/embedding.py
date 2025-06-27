from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


def split_to_chunks(full_profile):
    docs = [
        Document(page_content=full_profile, metadata={"source": "profile_json"}),
    ]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs_split = text_splitter.split_documents(docs)
    return docs_split


def load_embeddings():
    logger.info('Loading Embedding')
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    logger.info('Done')
    return embeddings
