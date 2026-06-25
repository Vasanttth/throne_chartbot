"""
chatbot.py
RAG chatbot for Throne Recliners using TXT knowledge base only.
Uses Groq API instead of Ollama.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

VECTORSTORE_PATH = "vectorstore"
COLLECTION_NAME = "throne_recliners"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.1-8b-instant"


PROMPT_TEMPLATE = """
You are the official AI assistant for Throne Recliners.

Answer customer questions using ONLY the retrieved knowledge base context.

Rules:
1. Use only the retrieved context.
2. Understand the meaning of the customer question, even if the wording is different.
3. If the information exists in the context, answer naturally and clearly.
4. Do not invent prices, warranty periods, product names, offers, locations, phone numbers, or emails.
5. Do not say "refer to website" unless the context says so.
6. If the information is not available in the context, reply exactly:
"I couldn't find that information in the Throne Recliners knowledge base."

Retrieved Context:
{context}

Conversation:
{chat_history}

Customer Question:
{question}

Assistant Answer:
"""


def load_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )

    llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=700,
   )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=4,
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "chat_history", "question"],
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        verbose=False,
    )

    return chain