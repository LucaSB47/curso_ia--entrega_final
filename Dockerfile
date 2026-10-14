# Usamos Python 3.12 slim como base
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del proyecto
COPY . .

# Exponer el puerto donde corre FastAPI
EXPOSE 8000

# Comando por defecto para iniciar la API con Uvicorn
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]