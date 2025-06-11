# Importations des bibliothèques nécessaires
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from .config import settings

# ====== IMPORTATION ET ENCODAGE DE LA LABEL ======
def load_and_encode_data():
    # Chargement des données
    supply = pd.read_excel(settings.DATASET_PATH)
    print("Jeu de données importé✅✅")

    # Séparation des caractéristiques et de la cible
    x = supply.drop(columns=["Delivery_Status"])  # Features
    y = supply["Delivery_Status"]  # Target

    # Encodage du label
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Division des données en ensembles d'entraînement et de test
    x_train, x_test, y_train, y_test = train_test_split(
        x, y_encoded, random_state=settings.RANDOM_STATE, test_size=settings.TEST_SIZE
    )

    return x_train, x_test, y_train, y_test, supply