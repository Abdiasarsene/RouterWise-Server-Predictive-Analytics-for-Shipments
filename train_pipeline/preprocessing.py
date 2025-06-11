# Importation des bibliothèques nécessaires
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from category_encoders import CatBoostEncoder

# ====== PRETRAITEMENT DES DONNEES ======
def get_preprocessor(supply):
    # Séparation des types de données
    features = supply.drop(columns=["Delivery_Status"])
    num_col = features.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_col = features.select_dtypes(include=["object"]).columns.tolist()

    # Colonnes numériques
    num_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler()),
    ])

    # Colonnes catégorielles
    cat_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('oneencoder', CatBoostEncoder())
    ])

    # ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_col),
            ('cat', cat_transformer, cat_col)
        ]
    )

    return preprocessor