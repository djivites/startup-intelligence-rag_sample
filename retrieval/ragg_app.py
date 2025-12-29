import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import ollama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Startup Intelligence Assistant",
    page_icon="🚀",
    layout="wide"
)

st.title("Startup – Funder Intelligence Hub")
st.caption("AI-powered startup & investment intelligence system")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Session Settings")
    session_id = st.text_input("Session ID", value="default_session")
    st.markdown("---")
    st.markdown("**Vector Store:** ChromaDB")
    st.markdown("**Mode:** Retrieval-Augmented Generation")

# ---------------- CORE SETUP ----------------
CHROMA_PATH = "chroma_db"
MODEL_NAME = "llama3"

if "store" not in st.session_state:
    st.session_state.store = {}

llm = ollama.Ollama(model=MODEL_NAME)
embeddings = OllamaEmbeddings(model=MODEL_NAME)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# ---------------- HELPER: FORMAT DOCS ----------------
def format_docs(docs):
    formatted = []
    for doc in docs:
        meta = "\n".join([f"{k}: {v}" for k, v in doc.metadata.items()])
        formatted.append(
            f"""
--- DOCUMENT ---
METADATA:
{meta}

CONTENT:
{doc.page_content}
"""
        )
    return "\n\n".join(formatted)


# ---------------- PROMPTS ----------------
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "Rephrase the user question clearly if needed."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

system_prompt = (
    "You are an expert startup intelligence assistant.\n"
    "You must answer using ONLY the provided context.\n\n"
    "ellobarate and explain the anser well\n\n"
    "Each document includes metadata and content.\n"
    "Use both metadata and content to answer accurately.\n\n"
    "If information is missing and not related to context, say so clearly.\n\n"
    "Format your answer as:\n"
    "Answer:\n"
    "<answer>\n\n"
    "Reasoning:\n"
    "<why this answer is correct>\n\n"
    "Evidence:\n"
    "<quoted text or metadata>\n\n"
    "Source url:available in the context give the first 3 unique url\n\n"
    "Confidence: High / Medium / Low\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
   
    ("human", "{input}")
])

# --------- CUSTOM RAG CHAIN (IMPORTANT) ----------
def custom_qa_chain(inputs):
    docs = inputs["context"]
    formatted_context = format_docs(docs)
    print(formatted_context)
    prompt = qa_prompt.format(
        context=formatted_context,
        input=inputs["input"]
    )

    return llm.invoke(prompt)

# ---------------- RAG PIPELINE ----------------
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

rag_chain = create_retrieval_chain(
    history_aware_retriever,
    custom_qa_chain
)

def get_session_history(session_id):
    if session_id not in st.session_state:
        st.session_state[session_id] = ChatMessageHistory()
    return st.session_state[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer"   # <-- ADD THIS LINE
)


# ---------------- CHAT UI ----------------
st.divider()

user_input = st.chat_input("Ask about startups, funding, investors...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Analyzing..."):
        response = conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )

    with st.chat_message("assistant"):
        st.markdown(response["answer"])

    with st.expander("🧠 Conversation History"):
        history = get_session_history(session_id)
        for msg in history.messages:
            st.markdown(f"**{msg.type.capitalize()}:** {msg.content}")

