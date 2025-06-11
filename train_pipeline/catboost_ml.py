# 📦 Importation des bibliothèques
import os
import mlflow
import bentoml
import logging
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score
from catboost import CatBoostClassifier, Pool
from sklearn.preprocessing import LabelEncoder

# 🌍 Variables d'environnement
load_dotenv()
dataset_path = os.getenv("TRAIN_DATASET_PATH")
mlflow_experiment = os.getenv("EXPERIMENT_NAME_TWO")
mlflow_tracking = os.getenv("MFLOW_TRACKING_URI")

# 🔧 Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📥 Chargement des données
data = pd.read_excel(dataset_path)
logger.info("✅ Données chargées")

# 🧪 Séparation features / cible
X = data.drop(columns=["Delivery_Status"])
y = LabelEncoder().fit_transform(data["Delivery_Status"])

# 🔍 Identifier les colonnes catégorielles
cat_cols = X.select_dtypes(include="object").columns.tolist()
X[cat_cols] = X[cat_cols].fillna('missing')

# ✂️ Split entraînement / test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Remplacer les NaN dans les colonnes catégorielles pour chaque split
X_train.loc[:, cat_cols] = X_train[cat_cols].fillna('missing')
X_test.loc[:, cat_cols] = X_test[cat_cols].fillna('missing')

# 🎯 Initialisation du modèle CatBoost
model = CatBoostClassifier(
    iterations=300,
    learning_rate=0.1,
    depth=6,
    verbose=0,
    random_seed=42
)

# 📦 Création du Pool avec informations de colonnes catégorielles
train_pool = Pool(X_train, y_train, cat_features=cat_cols)
test_pool = Pool(X_test, y_test, cat_features=cat_cols)

# 🏋️‍♂️ Entraînement du modèle
model.fit(train_pool)
logger.info("✅ Modèle CatBoost entraîné")

# 📈 Fonction de prédiction + tracking MLflow + enregistrement
def predict_log_save(model, test_pool, y_test, model_name):
    mlflow.set_tracking_uri(mlflow_tracking)
    mlflow.set_experiment(mlflow_experiment)

    try:
        y_pred = model.predict(test_pool)
        acc = accuracy_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)

        with mlflow.start_run(run_name=model_name):
            mlflow.log_param("model_type", model_name)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("recall", rec)

            # 🔒 Sauvegarde du modèle MLflow
            mlflow.catboost.log_model(model, model_name)
            logger.info(f"✅ Modèle {model_name} loggé dans MLflow")

            # 📦 Enregistrement dans le Registry
            model_uri = f"run:/{mlflow.active_run().info.run_id}/{model_name}"
            result = mlflow.register_model(model_uri=model_uri, name=model_name)

            client = mlflow.tracking.MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=result.version,
                stage="Production",
                archive_existing_versions=True
            )
            logger.info(f"🎯 Modèle {model_name} promu en Production dans le Model Registry")

            # 🥡 Sauvegarde avec BentoML
            bentoml.catboost.save_model(model_name, model)
            logger.info(f"✅ Modèle {model_name} sauvegardé avec BentoML")

    except Exception as e:
        logger.error(f"❌ Erreur pendant le logging de {model_name} : {e}")

# 🚀 Exécution de la fonction
predict_log_save(model, test_pool, y_test, model_name="catboost_delivery_status")