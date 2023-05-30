# Utilisez une image python de base
FROM python:3.10.11-slim-buster

# Spécifiez le répertoire de travail
WORKDIR /app

# Cloner le dépôt git dans le conteneur
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y libglib2.0-dev && \
    apt-get install -y libpango1.0-0

# Copie des models
COPY db_mobilenet_v3_large-fd62154b.pt /root/.cache/doctr/models/db_mobilenet_v3_large-fd62154b.pt
COPY db_resnet50-ac60cadc.pt /root/.cache/doctr/models/db_resnet50-ac60cadc.pt
COPY crnn_vgg16_bn-9762b0b0.pt /root/.cache/doctr/models/crnn_vgg16_bn-9762b0b0.pt

# Installer les dépendances requises pour l'application
COPY api.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8016

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8016"]
