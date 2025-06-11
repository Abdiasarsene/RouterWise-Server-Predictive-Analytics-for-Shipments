# Importation des librairies
import mlflow
import logging
import asyncio
from fastapi import FastAPI,HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from app.schema import LogistikData
from app.config import Settings
from app.predictor import make_prediction
from app.model_loader import load_mlflow_model, load_bentoml_model

# ====== PARAMETRAGE ======
settings = Settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== CREATION DE L'API =====
app = FastAPI(
    title= settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# ====== INSTRUMENTATION  ======
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# ====== CONFIGURATION DE MLFLOW ======
mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

# ====== INITIALISATION DU MODELE ======
model = None
model_type = None

# ====== CHARGEMENT DU MODEL AVEC MLFLOW ET BENTOML(EN FALLBACK)
@app.on_event('startup')
async def startup_event():
    print("🚀 Démarrage de l'API FastAPI...")
    global model, model_type
    logger.info("✅ Lancement de l'API")
    try:
        model = await asyncio.wait_for(asyncio.to_thread(load_mlflow_model, settings.mlflow), timeout=10.0)
        model_type = "MLflow"
        logger.info("Modèle chargé via MLflow ✅")
    except Exception as e:
        logger.warning(f"❌ Erreur MLflow : {str(e)}\n")
        logger.info("Mode secours via BentoML activée")
        try:
            model = load_bentoml_model(settings.bentoml)
            model_type = "BentoML"
            logger.info("Modèle chargé via BentoML chargé en secours ✅")
        except Exception as bentoml_error:
            logger.critical(f"❌ BentoML échec : {str(bentoml_error)}")
            raise RuntimeError(f"Échec du chargement des modèles : {e} / {bentoml_error}")

# ====== PREDICTION ET INSERTION DES DONNEES ======
@app.post("/v1/predict")
async def predict_logistic(data: LogistikData):
    try:
        global model, model_type
        input_dict = data.dict(by_alias=True)
        predicted_class, message = make_prediction(model, model_type, input_dict)

        logger.info("📢 Données insérées avec succès")

        return {
            "Deliver Status": message,
            "Code": predicted_class,
            "Statut": "Success",
            "Model Used": model_type
        }

    except Exception as e:
        logger.error(f"Erreur de prédiction : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {str(e)}")