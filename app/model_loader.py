# app/model_loader.py
import mlflow
import bentoml
import logging

logger = logging.getLogger(__name__)

def load_mlflow_model(path):
    logger.info(f"🔄 Chargement MLflow depuis: {path}")
    model = mlflow.pyfunc.load_model(path)
    if model is None:
        raise RuntimeError("⚠️ Échec MLflow.")
    return model

def load_bentoml_model(tag):
    logger.info("🔄 Chargement via BentoML...")
    model = bentoml.sklearn.load_model(tag)
    if model is None:
        raise RuntimeError("⚠️ Échec BentoML.")
    return model
