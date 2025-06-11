# main.py
from fastapi import FastAPI
from app.config import Settings
from app.model_loader import load_mlflow_model, load_bentoml_model
import logging

app = FastAPI()

settings = Settings()
model = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    global model
    logger.info("🚀 Démarrage de l'API...")
    print("🚀 Démarrage de l'API...")

    if settings.mlflow:
        logger.info("🧠 Chargement du modèle MLflow...")
        model = load_mlflow_model(settings.mlflow)
    elif settings.bentoml:
        logger.info("🧠 Chargement du modèle BentoML...")
        model = load_bentoml_model(settings.bentoml)
    else:
        logger.error("❌ Aucun modèle n’a été spécifié dans les variables d’environnement.")
        raise RuntimeError("❌ Aucun modèle n’a été spécifié.")

    logger.info("✅ Modèle chargé avec succès")
    print("✅ Modèle chargé avec succès")

@app.get("/")
def root():
    print("✅ Endpoint racine appelé")
    return {"message": "L'API SupplyChain est opérationnelle."}

@app.get("/test-model")
def test_model():
    if model is None:
        raise RuntimeError("❌ Modèle non chargé.")
    return {"status": "Modèle disponible et chargé"}
