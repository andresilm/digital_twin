from langchain.vectorstores import FAISS


def create_index(docs_split, embeddings):
    return FAISS.from_documents(docs_split, embeddings)
