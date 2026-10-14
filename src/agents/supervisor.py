from typing import Literal, TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from src.config import settings
from src.rag.vectorstore import buscar_documentacion_tecnica

# Definición del Estado del Grafo
class State(TypedDict):
    messages: List[BaseMessage]
    dispositivo: str
    sintomas: str
    documentacion_recuperada: str
    diagnostico_final: str

# Modelo LLM Asíncrono
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=settings.OPENAI_API_KEY
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
    return {"diagnostico_final": response.content}

# Enrutamiento del Supervisor
def supervisor_router(state: State) -> Literal["nodo_rag", "nodo_analista_hardware"]:
    if not state.get("documentacion_recuperada"):
        return "nodo_rag"
    return "nodo_analista_hardware"

def construir_grafo(checkpointer):
    workflow = StateGraph(State)
    
    workflow.add_node("nodo_rag", nodo_rag)
    workflow.add_node("nodo_analista_hardware", nodo_analista_hardware)
    
    workflow.add_edge(START, "nodo_rag")
    workflow.add_edge("nodo_rag", "nodo_analista_hardware")
    workflow.add_edge("nodo_analista_hardware", END)
    
    return workflow.compile(checkpointer=checkpointer)