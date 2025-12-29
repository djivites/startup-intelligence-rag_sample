from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import ollama
CHROMA_PATH = "chroma_db"
MODEL_NAME = "llama3"

llm = ollama.Ollama(model=MODEL_NAME)
embeddings = OllamaEmbeddings(model=MODEL_NAME)
vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)
docs = vectorstore.similarity_search("Bianca Cefalo founded Space DOTs, a company that detects", k=4)
for d in docs:
    print("----")
    print(d.page_content)
   