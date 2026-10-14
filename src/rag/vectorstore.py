from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.config import settings

async def get_vector_store():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
        pinecone_api_key=settings.PINECONE_API_KEY
    )
    return vectorstore

async def buscar_documentacion_tecnica(query: str, k: int = 3) -> str:
    """Busca en los manuales de hardware vectorizados en Pinecone."""
    vectorstore = await get_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = await retriever.ainvoke(query)
    
    if not docs:
        return "No se encontró documentación técnica específica para este caso."
    
    contexto = "\n\n".join([doc.page_content for doc in docs])
    return contexto