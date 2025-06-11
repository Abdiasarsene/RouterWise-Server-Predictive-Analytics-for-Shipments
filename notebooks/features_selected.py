import os
import shap
import eli5
import logging
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import RFE
from category_encoders import CatBoostEncoder
from sklearn.compose import ColumnTransformer
from eli5.sklearn import PermutationImportance
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, RobustScaler, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold, RFE, chi2, SelectKBest

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Initialisation et chargement des données
load_dotenv()
data_path = os.getenv("DATASET_PATH")
data = pd.read_excel(data_path)

# Séparation features/target
x = data.drop(columns=['Delivery_Status'])
y = LabelEncoder().fit_transform(data['Delivery_Status'])

# Train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Colonnes numériques/catégorielles
numeric_cols = x_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = x_train.select_dtypes(include=['object']).columns.tolist()

# Pipelines
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('outilier', RobustScaler()),
    ('variance_selector', VarianceThreshold(threshold=0.1)),
])
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', CatBoostEncoder()), 
    ('scaler', MinMaxScaler()),
    ('chi2_selector', SelectKBest(score_func=chi2, k='all'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_cols),
    ('cat', categorical_pipeline, categorical_cols)
])

# Prétraitement
x_train_preprocessed = preprocessor.fit_transform(x_train, y_train)
x_test_preprocessed = preprocessor.transform(x_test)

# 2. Récupérer les noms de features transformées
def get_transformed_feature_names(preprocessor, numeric_cols, categorical_cols):
    feature_names = []

    # Numériques après variance threshold
    num_selector = preprocessor.named_transformers_['num'].named_steps['variance_selector']
    num_support = num_selector.get_support()
    numeric_selected = np.array(numeric_cols)[num_support]
    feature_names.extend(numeric_selected)

    # Catégorielles après chi2
    cat_selector = preprocessor.named_transformers_['cat'].named_steps['chi2_selector']
    cat_support = cat_selector.get_support()
    categorical_selected = np.array(categorical_cols)[cat_support]
    feature_names.extend(categorical_selected)

    return feature_names

# Obtenir noms des colonnes transformées et sélectionnées
transformed_features = get_transformed_feature_names(preprocessor, numeric_cols, categorical_cols)

# 3. Application de RFE
rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf = rf.fit(x_train_preprocessed, y_train)
rfe = RFE(estimator=model_rf, n_features_to_select=10)
rfe.fit(x_train_preprocessed, y_train)

# Récupération des features finales retenues par RFE
final_features = np.array(transformed_features)[rfe.support_]
x_train_rfe = rfe.transform(x_train_preprocessed)
x_test_rfe = rfe.transform(x_test_preprocessed)

# Affichage des features finales retenues
logging.info("✅ Features finales retenues par RFE : %s", final_features)

# 4. Permutation Importance
rf.fit(x_train_rfe, y_train)
perm = PermutationImportance(rf, scoring='accuracy', random_state=42)
perm.fit(x_train_rfe, y_train)

# Afficher les importances
logging.info("\n🎯 Importance des features selon Permutation Importance :")
eli5.show_weights(perm, feature_names=final_features.tolist())

# Ajout du SHAP
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(x_test_rfe)
shap.summary_plot(shap_values, x_test_rfe, feature_names=final_features)

# Exportaation des features sélectionnées et leur importance 
pd.DataFrame({
    'feature': final_features,
    'importance': perm.feature_importances_
}).sort_values(by='importance', ascending=False).to_excel('./dataset/features_selected.xlsx', index=False)
logging.info("✅ Fichier 'features_selected.csv' créé avec succès.")
# Fin du script