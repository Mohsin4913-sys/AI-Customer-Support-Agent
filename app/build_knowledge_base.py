from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Find all text files in the knowledge base
knowledge_base_path = Path("knowledge_base")

documents = []

for file_path in knowledge_base_path.glob("*.txt"):
    loader = TextLoader(str(file_path))
    documents.extend(loader.load())


print("Documents loaded:", len(documents))


# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=40
)

chunks = text_splitter.split_documents(documents)

print("Chunks created:", len(chunks))


# Create embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create/update Chroma vector database
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="customer_support",
    persist_directory="vector_db"
)

print("Knowledge base created successfully.")