import os
import joblib
import tempfile
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def create_sample_data():
    # Création d'un petit jeu de données
    np.random.seed(42)
    X = np.random.rand(100, 4)
    y = np.random.randint(0, 2, 100)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def build_pipeline():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(solver="liblinear"))
    ])

def test_model_save_and_load_with_joblib():
    X_train, X_test, y_train, y_test = create_sample_data()
    model = build_pipeline()
    model.fit(X_train, y_train)

    original_preds = model.predict(X_test)

    with tempfile.TemporaryDirectory() as tmp_dir:
        model_path = os.path.join(tmp_dir, "test_model.joblib")
        
        # Enregistrement
        joblib.dump(model, model_path)
        assert os.path.exists(model_path), "Le fichier du modèle n’a pas été enregistré"

        # Chargement
        loaded_model = joblib.load(model_path)
        loaded_preds = loaded_model.predict(X_test)

        # Vérification d'identité des prédictions
        assert np.array_equal(original_preds, loaded_preds), "Les prédictions ne correspondent pas après chargement"

        # Vérification simple d'exactitude
        acc = accuracy_score(y_test, loaded_preds)
        assert acc > 0, "Le modèle chargé a une précision nulle"
