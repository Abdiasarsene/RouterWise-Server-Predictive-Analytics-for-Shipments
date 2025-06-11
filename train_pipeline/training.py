# Importation des bibliothèques nécessaires
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from .config import settings

# ====== CREATION DES PIPELINES ======
def train_models(x_train, y_train, preprocessor):
    models ={
        "logistic" : LogisticRegression(max_iter=1000, solver='liblinear', class_weight="balanced"),
        "random_forest" : RandomForestClassifier(),
    }
    
    param_dist ={
        "logistic":{
            'classifier__C': [0.1, 1, 10],
            'classifier__penalty': ["l1", "l2"]
        },
        "random_forest":{
            'classifier__n_estimators': [100, 200, 300],
            'classifier__max_depth': [3, 6, 10],
            'classifier__min_samples_split': [2, 5, 10]
        },
    }
    
    best_models = {}
    cv = StratifiedKFold(n_splits=settings.N_SPLITE, shuffle=True, random_state=settings.RANDOM_STATE)
    
    for name, model in models.items():
        print(f"\n Entraînement du modèle : {name}")
        
        pipe = Pipeline([
            ('preprocessing', preprocessor),
            ('classifier', model)
        ])
        
        search = RandomizedSearchCV(
            pipe,
            param_distributions=param_dist[name],
            n_iter=20,
            cv=cv,
            n_jobs=-1,
            scoring='accuracy',
            random_state=settings.RANDOM_STATE
        )
        
        search.fit(x_train, y_train)
        best_models[name] = search.best_estimator_
        
    print("Entraînement mis en place ✅✅")
    return best_models