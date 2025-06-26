import requests
from fastapi import FastAPI
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from pydantic import BaseModel

app = FastAPI()


class Query(BaseModel):
    message: str


@app.on_event("startup")
async def startup_event():
    loader_pdf = PyPDFLoader("data_ingestion/resume.pdf")
    loader_txt = TextLoader("data_ingestion/personal.txt")
    docs = loader_pdf.load() + loader_txt.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_split = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    global vectordb
    vectordb = FAISS.from_documents(docs_split, embeddings)


@app.post("/query")
async def query_rag(input: Query):
    docs = vectordb.similarity_search(input.message, k=1)
    context = docs[0].page_content if docs else ""
    response = requests.post("http://llm-service:8083/complete", json={
        "user_input": input.message,
        "context": context
    })
    return response.json()
