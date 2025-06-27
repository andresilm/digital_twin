import requests
from fastapi import FastAPI
import json
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from pydantic import BaseModel, Field

app = FastAPI()


class Query(BaseModel):
    message: str = Field(..., max_length=1000, description="Texto del usuario (máx. 1000 caracteres)")


def json_to_text(data, indent=0):
    text = ""
    prefix = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            text += f"{prefix}{key}:\n"
            text += json_to_text(value, indent + 1)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            text += f"{prefix}- "
            # Para listas, no aumentamos indent en la línea de guion para mejor legibilidad
            if isinstance(item, (dict, list)):
                text += "\n" + json_to_text(item, indent + 1)
            else:
                text += f"{item}\n"
    else:
        text += f"{prefix}{data}\n"
    return text


base_profile = ""


@app.on_event("startup")
async def startup_event():
    with open("data_ingestion/profile.json", "r", encoding="utf-8") as f:
        profile_json = json.load(f)

    profile_text = json_to_text(profile_json)

    global base_profile_text
    with open("data_ingestion/base_profile.txt", "r", encoding="utf-8") as f:
        base_profile_text = f.read()

    docs = [
        Document(page_content=profile_text, metadata={"source": "profile_json"}),
    ]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs_split = text_splitter.split_documents(docs)
    print('Loading Embedding')
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    print('Done')
    global vectordb
    vectordb = FAISS.from_documents(docs_split, embeddings)


@app.post("/query")
async def query_rag(input: Query):
    docs = vectordb.similarity_search(input.message, k=1)
    print(docs)
    context = docs[0].page_content if docs else ""
    response = requests.post("http://llm-service:8083/complete", json={
        "user_input": input.message,
        "base_profile": base_profile_text,
        "context": context
    })
    return response.json()
