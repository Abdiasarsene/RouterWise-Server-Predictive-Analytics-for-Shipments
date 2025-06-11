from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

# Exemple de payload conforme à ton modèle LogistikData
valid_payload = {
    "Stock_Level": 250,
    "Sales": 80,
    "Transportation_Cost": 75.5,
    "Region": "East",
    "Delivery_Urgency": "On Time",
    "Estimated_Day": 5
}

def test_predict_success():
    with TestClient(app) as client:
        response = client.post("/v1/predict", json=valid_payload)
        assert response.status_code == 200

def test_predict_invalid_payload():
    # Envoi d'un payload incomplet ou mal formé
    invalid_payload = {
        "Stock_Level": "invalid_string",
        # autres champs manquants
    }
    response = client.post("/v1/predict", json=invalid_payload)
    assert response.status_code == 422  # Validation error de FastAPI

def test_api_root():
    response = client.get("/")
    # Si tu as une route racine, sinon tu peux l'adapter ou la supprimer
    assert response.status_code in [200, 404]
