import os
import json
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import ollama


# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
DATA_DIR = os.path.join(BASE_DIR, "data") 
RAW_DIR = os.path.join(DATA_DIR, "raw", "news") 
DATA_DIR = os.path.join(DATA_DIR, "processed") 
CHROMA_DIR = "chroma_db"
EMBED_MODEL = "llama3"
# ========================================


def load_documents():
    documents = []

    for file in os.listdir(DATA_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(DATA_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        full_text = f"""
Startup Name: {data['metadata'].get('startup_name', '')}
Investor: {data['metadata'].get('investor_name', '')}
Funding Stage: {data['metadata'].get('funding_stage', '')}

Summary:
{data['state_summary']}

Evidence:
{" ".join(data['evidence'])}

Keywords:
{"".join(data['keywords'])}
"""

        documents.append(
            Document(
                page_content=full_text,
                metadata=data.get("metadata", {})
            )
        )

    return documents



def build_vector_db():
    print("🔄 Loading documents...")
    docs = load_documents()

    print(f"📄 Total chunks created: {len(docs)}")

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        
    )

    vectordb.add_documents(docs)
    vectordb.persist()

    print("✅ ChromaDB built successfully!")
    return vectordb


def query_rag(query: str, k: int = 5):
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings

    )

    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)

    print("\n🔍 Retrieved Context:\n")
    for i, doc in enumerate(docs, 1):
        print(f"--- Chunk {i} ---")
        print(doc.page_content[:400])
        print("Metadata:", doc.metadata)
        print("-" * 50)

    return docs


# ================= MAIN =================
if __name__ == "__main__":
    # Step 1: Build DB (run once or when data updates)
    build_vector_db()

    
