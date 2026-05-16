FROM nvidia/cuda:12.1-runtime-ubuntu22.04

# Installation de Python et des dépendances système
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie des dépendances
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copie de l'application
COPY . .

# Exposition des ports (API, Dashboard, n8n)
EXPOSE 8000 8501 5678

# Commande de démarrage (API par défaut)
CMD ["python3", "-m", "uvicorn", "core.engine:app", "--host", "0.0.0.0", "--port", "8000"]
