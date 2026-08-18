from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load existing vector database
vector_store = Chroma(
    collection_name="customer_support",
    persist_directory="vector_db",
    embedding_function=embeddings
)


@tool
def search_knowledge_base(question: str) -> str:
    """
    Search the customer-support knowledge base for information
    about company policies, refunds, shipping, returns, and FAQs.
    """

    results = vector_store.similarity_search(
        question,
        k=3
    )

    if not results:
        return "No relevant information was found."

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    return context


if __name__ == "__main__":

    question = "How long do I have to get a refund?"

    result = search_knowledge_base.invoke({
        "question": question
    })

    print("\nQuestion:")
    print(question)

    print("\nRetrieved Context:")
    print(result)