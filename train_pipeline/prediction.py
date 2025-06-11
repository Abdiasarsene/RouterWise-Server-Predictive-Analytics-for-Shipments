# Importation des bibliothèques nécessaires
import mlflow
import bentoml
from .config import settings
from sklearn.metrics import accuracy_score, f1_score, recall_score

def log_and_save_models(best_models, x_test, y_test):
    """
    Fonction pour enregistrer les modèles dans MLflow et BentoML.
    
    :param best_models: Dictionnaire des meilleurs modèles entraînés.
    :param x_test: Données de test pour évaluer les modèles.
    :param y_test: Cibles de test pour évaluer les modèles.
    """
    mlflow.set_experiment(settings.EXPERIMENT_NAME)
    
    for model_name, model in best_models.items():
        try:
            # Prédiction et calcul des métriques
            y_pred = model.predict(x_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
            rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)

            with mlflow.start_run(run_name=model_name):
                # Log des paramètres et métriques dans MLflow
                mlflow.log_param('model_type', model_name)
                mlflow.log_params(model.get_params())
                mlflow.log_metric('accuracy', acc)
                mlflow.log_metric('f1_score', f1)
                mlflow.log_metric('recall', rec)

                # Enregistrement du modèle dans MLflow
                mlflow.sklearn.log_model(model, model_name)
                print(f"✅ Modèle {model_name} enregistré avec MLflow.")

                # Enregistrement du modèle dans le Model Registry
                model_uri = f"run:/{mlflow.active_run().info.run_id}/{model_name}"
                result = mlflow.register_model(model_uri=model_uri, name=model_name)

                client = mlflow.tracking.MlflowClient()
                client.transition_model_version_stage(
                    name=model_name,
                    version=result.version,
                    stage="Production",
                    archive_existing_versions=True
                )
                print(f"🎯 {model_name} promu en Production dans le Model Registry.")

            # Enregistrement avec BentoML
            bentoml.sklearn.save_model(model_name, model)
            print(f"💾 Modèle {model_name} sauvegardé avec BentoML.")

        except Exception as e:
            print(f"⚠️ Erreur lors de l'enregistrement du modèle {model_name}: {e}")