# Importation des bibliothèques nécessaires
from train_pipeline.data_loader import load_and_encode_data
from train_pipeline.preprocessing import get_preprocessor
from train_pipeline.training import train_models
from train_pipeline.prediction import log_and_save_models

# Fonction principale pour exécuter le pipeline d'entraînement
if __name__ == "__main__":
    # Chargement et encodage des données
    x_train, x_test, y_train, y_test, supply = load_and_encode_data()
    
    # Prétraitement des données
    preprocessor = get_preprocessor(supply)
    
    # Entraînement des modèles
    best_models = train_models(x_train, y_train, preprocessor)
    
    # Enregistrement des modèles dans MLflow et BentoML
    log_and_save_models(best_models, x_test, y_test)