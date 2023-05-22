# Utilisez une image python de base
FROM python:3.10.11-slim-buster

# Spécifiez le répertoire de travail
WORKDIR /app

# Cloner le dépôt git dans le conteneur
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y libglib2.0-dev && \
    apt-get install -y libpango1.0-0

# Installer les dépendances requises pour l'application
COPY api.py .
COPY requirement.txt .
RUN pip install -r requirement.txt

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
