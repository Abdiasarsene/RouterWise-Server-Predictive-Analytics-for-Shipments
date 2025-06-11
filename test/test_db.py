from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/logistik_data"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("✅ Connexion réussie à la base de données MySQL")
except Exception as e:
    print(f"❌ Échec de connexion : {e}")
