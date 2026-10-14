from fastapi import FastAPI, HTTPException
from langgraph.checkpoint.memory import MemorySaver
from src.api.schemas import SoporteRequest, DiagnosticoResponse
from src.agents.supervisor import construir_grafo
from langchain_core.messages import HumanMessage

app = FastAPI(
    title="The Intelligence System - Hardware Support API",
    version="1.0.0",
    description="Sistema multi-agente con RAG y Supervisor para diagnóstico técnico avanzado."
)

# Inicializamos el Checkpointer en memoria (o SQLiteSaver para persistencia en disco)
memory = MemorySaver()
graph = construir_grafo(checkpointer=memory)

@app.post("/diagnosticar", response_model=DiagnosticoResponse)
async def diagnosticar_problema(request: SoporteRequest, thread_id: str = "default_session"):
    try:
        config = {"configurable": {"thread_id": thread_id}}
        
        initial_state = {
            "messages": [HumanMessage(content=request.sintomas)],
            "dispositivo": request.dispositivo,
            "sintomas": request.sintomas,
            "documentacion_recuperada": "",
            "diagnostico_final": ""
        }
        
        # Ejecución asíncrona del grafo respetando el checkpointer
        final_state = await graph.ainvoke(initial_state, config=config)
        
        # Parseo de salida estructurado
        return DiagnosticoResponse(
            diagnostico_preliminar=final_state.get("diagnostico_final", "Sin diagnóstico"),
            pasos_a_seguir=["1. Revisar voltajes con multímetro", "2. Verificar códigos en manual técnico", "3. Proceder según guía"],
            componentes_afectados=[request.dispositivo],
            nivel_criticidad="Medio",
            herramientas_necesarias=["Multímetro", "Programador CH341A"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))