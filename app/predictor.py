import pandas as pd
from fastapi import HTTPException

logistik_mapping = {0: "On Time", 1: "Late"}

def make_prediction(model, model_type: str, input_dict: dict) -> tuple:
    df = pd.DataFrame([input_dict])
    if model_type in ["MLflow", "BentoML"]:
        prediction = model.predict(df)
        predicted_class = int(prediction[0])
        message = f"Your delivery status prediction is: {logistik_mapping.get(predicted_class, 'Unknown')}. Stay informed and plan accordingly!"
        return predicted_class, message
    raise HTTPException(status_code=500, detail="Modèle non initialisé correctement")
