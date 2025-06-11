# Etape 1 : Utiliser une image officielle Python
FROM python:3.10-slim

# Etape 2 : Variable d'environnement de base 
ENV PYTHONDONTWRITEBYTECODE =1 \
    PYTHONUNBUFFERED =1 \
    PIP_NO_CACHE_DIR =1

# Etape 3 : Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Etape 4 : Définir le répétoire de travail 
WORKDIR /app

# Etape 5 : Copier uniquement requirements pour bénéficier du cache Docker
COPY requirements.txt

# Etape 6 : Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Etape 7 : Copier tout le reste du projet
COPY . .

# Etape 8 : Créer un utilisatuer non-root pour la sécurité
RUN useradd -m user
USER user

# Etape 9 : Port exposé
EXPOSE 8000

# Etape 10 : Commande de lancement (modifiable via ENTRYPOINT si nécessaire)
CMD ["uvicorn", "main:app", "--host","0.0.0.0","--port","8000"]