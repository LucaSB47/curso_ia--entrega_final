import os
from typing import Literal, TypedDict, List
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from src.config import settings
from src.rag.vectorstore import buscar_documentacion_tecnica
from langchain_google_genai import ChatGoogleGenerativeAI

# Aseguramos la trazabilidad en LangSmith desde las variables de configuración
if getattr(settings, "LANGSMITH_API_KEY", None):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = getattr(
        settings, "LANGSMITH_PROJECT", "intelligence-hardware-support"
    )

# Definición del Estado del Grafo
class State(TypedDict):
    messages: List[BaseMessage]
    dispositivo: str
    sintomas: str
    documentacion_recuperada: str
    diagnostico_final: str

# Modelo LLM Asíncrono (Sin hard-coding: toma modelo y clave desde settings)
llm = ChatGoogleGenerativeAI(
    model=getattr(settings, "GEMINI_MODEL", "gemini-3.8-flash"),
    temperature=0.2,
    api_key=settings.GEMINI_API_KEY
)

async def nodo_rag(state: State):
    """Agente especialista en recuperar manuales y hojas de datos."""
    query = f"{state['dispositivo']} {state['sintomas']}"
    docs = await buscar_documentacion_tecnica(query)
    return {"documentacion_recuperada": docs}

async def nodo_analista_hardware(state: State):
    """Agente técnico que analiza los síntomas y la documentación para dar un veredicto."""
    prompt = f"""
    Eres un Ingeniero Experto en Reparación de Hardware y Soporte IT.
    Dispositivo: {state['dispositivo']}
    Síntomas reportados: {state['sintomas']}
    
    Documentación técnica de referencia recuperada:
    {state['documentacion_recuperada']}
    
    Genera un diagnóstico técnico detallado, los pasos de reparación recomendados (considerando uso de herramientas como multímetro, soldador, programador de BIOS si aplica) y las piezas afectadas.
    """
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    
    # Extraemos el string limpio si Gemini 3.8 devuelve una lista de bloques
    contenido = response.content
    if isinstance(contenido, list):
        texto_final = "".join(
            bloque.get("text", "") if isinstance(bloque, dict) else str(bloque)
            for bloque in contenido
        )
    else:
        texto_final = str(contenido)
        
    return {"diagnostico_final": texto_final}

# Enrutamiento dinámico del Supervisor
def supervisor_router(state: State) -> Literal["nodo_rag", "nodo_analista_hardware"]:
    if not state.get("documentacion_recuperada"):
        return "nodo_rag"
    return "nodo_analista_hardware"

def construir_grafo(checkpointer):
    workflow = StateGraph(State)
    
    workflow.add_node("nodo_rag", nodo_rag)
    workflow.add_node("nodo_analista_hardware", nodo_analista_hardware)
    
    # El Supervisor evalúa el estado y delega dinámicamente al nodo correspondiente
    workflow.add_conditional_edges(
        START,
        supervisor_router,
        {
            "nodo_rag": "nodo_rag",
            "nodo_analista_hardware": "nodo_analista_hardware"
        }
    )
    workflow.add_edge("nodo_rag", "nodo_analista_hardware")
    workflow.add_edge("nodo_analista_hardware", END)
    
    return workflow.compile(checkpointer=checkpointer)