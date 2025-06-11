# Dossier de tests : 
TEST_DIR = test

# ====== LANCER UN TEST SPÉCIFIQUE SUR LE PIPELINE MODELE======
test_pipeline:
	@echo "Lancement d'un test  ..."
	@py -m pytest $(TEST_DIR)/test_pipeline_model.py --maxfail=1 --disable-warnings -q

# ====== LANCER UN TEST SPÉCIFIQUE SUR L'API ======
test_api:
	@echo "Lancement d'un test sur les API ..."
	@py -m pytest $(TEST_DIR)/test_api.py --maxfail=1 --disable-warnings -q

# ====== TEST DE LA CONNECTION MYSQL ======
mysql_connection:
	@echo "Test de la connexion MySQL..."
	@py  $(TEST_DIR)/test_db.py 

# ======TEST REEL AVEC UN FICHIER DE TESTS========
predict:
	@echo "Debut du test"
	@py $(TEST_DIR)/test_predict.py

# ====== LINTING + FORMATAGE ======
lint: 
	@echo "Lancement du linting avec Ruff..."
	@ruff check . 

format :
	@echo "Formatage du code avec Ruf..."
	@ruff check . --fix

# ====== ENTRAINEMENT DU MODELE ======
train:
	@echo "Entrainement du modele..."
	@python model.py
	@echo "Entrainement termine"

# ====== ENTRAINEMENT DE CATBOOST ======
catboost :
	@echo "Lancement du pipeline CatBoost"
	@py catboost_ml.py

# ====== LANCER LE MONITORING ======
monitoring : 
	@echo "Lancement du monitoring"
	@py monitoring.py
	@echo "Monitoring lancé"

# ====== LANCER MLFLOW ======
mlflow_server:
	@echo "Lancement de MLflow"
	@mlflow ui

# ====== LANCER LE SERVEUR MySQL ======
mysql_server:
	@echo "Lancement du serveur MySQL..."
	@netstat -ano | findstr 3306

# ====== LANCER L'API ======
run:
	@echo "Lancement de l'API..."
	@uvicorn main:app --reload

