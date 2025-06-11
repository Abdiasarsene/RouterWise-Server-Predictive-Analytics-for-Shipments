import mysql.connector
import logging
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

def insert_data(data, Delivery_Status):
    try:
        with mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            if connection.is_connected():
                logging.info("✅ Connexion à MySQL réussie")
            
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO logistic_chain (
                    transportation_cost, 
                    distance_km, 
                    state,
                    delivery_urgency, 
                    urgency_level,  
                    client_type,
                    carrier_type,
                    transportation_method,
                    day_of_week,
                    weather_condition,
                    delivery_status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    data.transportation_cost,  
                    data.distance_km,
                    data.state,
                    data.delivery_urgency,
                    data.urgency_level,
                    data.client_type,
                    data.carrier_type,
                    data.transportation_method,
                    data.day_of_week,
                    data.weather_condition,
                    Delivery_Status
                )

                cursor.execute(insert_query, values)
                connection.commit()
                print("✅ Nouvelles données enregistrées avec succès")

    except mysql.connector.Error as err:
        logging.error(f"❌ MySQL Error: {err}")
        print(f"❌ Problème MySQL : {err}")

    except Exception as e:
        logging.error(f"❌ Erreur générale : {e}")
        print(f"❌ Erreur générale : {e}")
