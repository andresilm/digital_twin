import logging
import requests
from fastapi import FastAPI
from data_load import load_profile_from_json, load_base_profile
from embedding import load_embeddings, split_to_chunks
from vector_db import create_index, get_most_revelant_documents
from models import UserInput

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """
    FastAPI startup event handler.

    Loads and prepares all resources required for the RAG (Retrieval-Augmented Generation) system:
    - Loads the base profile text from file.
    - Loads the full profile JSON and converts it into text chunks.
    - Loads the embeddings model.
    - Creates a FAISS vector index over the chunks using the embeddings.

    Stores the base profile and the vector database instance in the application state for reuse.
    """
    base_profile = load_base_profile()
    full_profile = load_profile_from_json()
    docs_split = split_to_chunks(full_profile)
    embeddings = load_embeddings()
    vectordb = create_index(docs_split, embeddings)

    app.state.base_profile = base_profile
    app.state.vectordb = vectordb


@app.post("/query")
async def query_rag(input: UserInput):
    """
    POST endpoint to process user queries via RAG.

    Args:
        input (UserInput): A Pydantic model containing the user message.

    Process:
        - Uses the FAISS vector store to perform a similarity search on the user message,
          retrieving the most relevant chunk of the profile.
        - Logs the chosen relevant document chunk for debugging.
        - Calls the LLM service, passing the user input, base profile, and retrieved context chunk.
        - Returns the LLM's JSON response to the client.

    Returns:
        dict: The JSON response from the LLM service, typically containing the generated answer.
    """
    vectordb = app.state.vectordb
    base_profile = app.state.base_profile

    docs = get_most_revelant_documents(vectordb, input.message)

    logger.debug("Selected chunk with size %d: %s", len(docs[0].page_content), str(docs[0].page_content))
    context = "\n".join(doc.page_content for doc in docs) if docs else ""
    response = requests.post("http://llm-service:8083/complete", json={
        "user_input": input.message,
        "base_profile": base_profile,
        "context": context
    })
    return response.json()
