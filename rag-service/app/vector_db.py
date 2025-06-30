from langchain.vectorstores import FAISS

K_DOCS = 2


def create_index(docs_split, embeddings):
    return FAISS.from_documents(docs_split, embeddings)


def get_most_revelant_documents(vectordb, message):
    return vectordb.similarity_search(message, k=K_DOCS)
