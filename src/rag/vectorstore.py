from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import settings
from langchain_huggingface import HuggingFaceEmbeddings

# Modelo local gratuito de 768 dimensiones (no requiere API key)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# Inicializar cliente de Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)

# Conectar LangChain con Pinecone
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="text" 
)

async def buscar_documentacion_tecnica(query: str) -> str:
    """Busca en Pinecone los documentos más relevantes usando embeddings de Google."""
    docs = await vectorstore.asimilarity_search(query, k=3)
    
    if not docs:
        return "No se encontró documentación técnica relevante en la base de datos."
        
    return "\n\n".join([doc.page_content for doc in docs])