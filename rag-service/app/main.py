import logging

import requests
from fastapi import FastAPI

from data_load import load_profile_from_json, load_base_profile
from embedding import load_embeddings, split_to_chunks
from vector_db import create_index
from models import UserInput


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI()
base_profile = None
vectordb = None


@app.on_event("startup")
async def startup_event():
    global base_profile
    global vectordb

    base_profile = load_base_profile()
    full_profile = load_profile_from_json()
    docs_split = split_to_chunks(full_profile)
    embeddings = load_embeddings()
    vectordb = create_index(docs_split, embeddings)


@app.post("/query")
async def query_rag(input: UserInput):
    docs = vectordb.similarity_search(input.message, k=1)
    logger.debug("Chose this entry in profile.json as the most relevant: %s", str(docs))
    context = docs[0].page_content if docs else ""
    response = requests.post("http://llm-service:8083/complete", json={
        "user_input": input.message,
        "base_profile": base_profile,
        "context": context
    })
    return response.json()
