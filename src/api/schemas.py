from pydantic import BaseModel, Field
from typing import List, Optional

class SoporteRequest(BaseModel):
    dispositivo: str = Field(..., description="Ej: Laptop Lenovo ThinkPad T480, Placa Madre ASUS Prime H410M")
    sintomas: str = Field(..., description="Descripción detallada de la falla, códigos de bips o comportamiento.")
    codigo_error: Optional[str] = Field(None, description="Código de error específico si lo hay (ej. Pantalla Azul 0x0000007E)")

class DiagnosticoResponse(BaseModel):
    diagnostico_preliminar: str = Field(..., description="Análisis técnico de la causa raíz más probable.")
    pasos_a_seguir: List[str] = Field(..., description="Lista ordenada de pasos de diagnóstico o reparación (ej. multímetro, regrabar BIOS).")
    componentes_afectados: List[str] = Field(..., description="Componentes de hardware involucrados.")
    nivel_criticidad: str = Field(..., description="Bajo, Medio, Alto o Crítico.")
    herramientas_necesarias: List[str] = Field(..., description="Herramientas requeridas (multímetro, programador CH341A, estación de calor, etc.).")