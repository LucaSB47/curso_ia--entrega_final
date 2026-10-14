#!/bin/bash
echo "🛠️ Construyendo y levantando The Intelligence System..."
docker-compose up --build -d
echo "✅ Sistema corriendo en http://localhost:8000/docs"