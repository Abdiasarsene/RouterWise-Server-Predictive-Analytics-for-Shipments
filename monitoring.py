# Importation des bibliothèques
import os
import time
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from prometheus_client import Counter
from prometheus_client import Gauge, start_http_server

# ====== CHARGEMENT DES PARAMETRES DEPUIS .env ======
load_dotenv()
dataset_path = os.getenv("TRAIN_DATASET_PATH")

# ====== DICTIONNAIRES DE METRIQUES ======
null_rate_metrics = {}
mean_metrics = {}
psi_metrics = {}

n_unique_metrics = {}
top_category_freq_metrics = {}

# ====== COMPTEUR D'ERREUR ======
error_counter = Counter("monitoring_errors", "Nombre d’erreurs lors du monitoring")

# ====== FONCTION DE CALCUL L'INDICE DE STABILITE DE LA POPULATION ======
def calculate_psi(expected, actual, buckets=10): 
    def scale_range(series, bins) : 
        return np.histogram(series.dropna(), bins=bins)[0]/len(series.dropna())
    
    expected_perc = scale_range(expected, buckets)
    actual_perc = scale_range(actual, buckets)
    
    # POur éviter les division par 0
    psi_values = (expected_perc - actual_perc) * np.log((expected_perc + 1e-6)/(actual_perc + 1e-6))
    return np.sum(psi_values)

# ====== MONITORING LOOP ======
def monitor_data(batch_df, baseline_df):
    numeric_cols = batch_df.select_dtypes(include=np.number).columns
    cat_cols = batch_df.select_dtypes(include='object').columns
    
    # ====== FEATURES NUMERIQUES ======
    for col in numeric_cols: 
        # Crée les métriques si elles n'existent pas déjà
        if col not in null_rate_metrics: 
            null_rate_metrics[col] = Gauge(f"null_rate_{col}", f"Taux de valeurs nulles dans {col}")
            mean_metrics[col] = Gauge(f"mean_{col}", f"Moyenne de la feature {col}")
            psi_metrics[col] = Gauge(f"psi_{col}", f"PSI entre {col} et la baseline")
        
        null_rate_metrics[col].set(batch_df[col].isnull().mean())
        mean_metrics[col].set(batch_df[col].mean())
        
        if baseline[col].nunique() > 1 and batch_df[col].nunique() > 1:
            psi = calculate_psi(baseline[col], batch_df[col])
        else:
            psi = 0
        psi_metrics[col].set(psi)

    
    # ====== FEATURES CATEGORIELLES ======
    for col in cat_cols: 
        if col not in null_rate_metrics: 
            null_rate_metrics[col] = Gauge(f"null_rate_{col}", f"Taux de valeurs nulles dans {col}")
            n_unique_metrics[col] = Gauge(f"n_unique_{col}", f"Nombre de modalités unique pour {col}")
            top_category_freq_metrics[col] = Gauge(f"top_category_freq_{col}", f"Fréquence de la modalité dominante pour {col}")
            
            null_rate_metrics[col].set(batch_df[col].isnull().mean())
            
            # Nombre de modalité unique
            n_unique_metrics[col].set(batch_df[col].nunique())
            
            # Modalité la plus fréquente (et sa fréquence)
            top_category = batch_df[col].mode().iloc[0] if not batch_df[col].mode().empty else "NA"
            top_freq = (batch_df[col]  == top_category).mean()
            top_category_freq_metrics[col].set(top_freq)

if __name__ == "__main__" : 
    start_http_server(8001)
    print("✅ Monitoring Prometheus lancé sur  : 8001")
    
    baseline = pd.read_excel(dataset_path)
    
    while True: 
        try: 
            batch = pd.read_excel(dataset_path)
            monitor_data(batch, baseline)
            print("✅ Batch analysé et metrics exposées")
        except FileNotFoundError: 
            error_counter.inc()
            print("⚠️ Fichier batch non trouvé, nouvelle tentative dans 1 min")
        time.sleep(60)