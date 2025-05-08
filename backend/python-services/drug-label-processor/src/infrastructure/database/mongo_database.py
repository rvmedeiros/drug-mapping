import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnections:
    def __init__(self):
        mongo_db_name = os.getenv("MONGO_DB_NAME")
        if not mongo_db_name:
            raise ValueError("Environment variable MONGO_DB_NAME is not defined")
        
        self.mongo_client = MongoClient(
            host=os.getenv("MONGO_HOST", "localhost"),
            port=int(os.getenv("MONGO_PORT", "27017")),
            username=os.getenv("MONGO_USER"),
            password=os.getenv("MONGO_PASSWORD"),
            authSource=os.getenv("MONGO_AUTH_DB", "admin"),
            authMechanism='SCRAM-SHA-256',
            serverSelectionTimeoutMS=5000
        )
        self.mongo_db = self.mongo_client[mongo_db_name]

    def close(self):
        self.mongo_client.close()
        
db_instance = DatabaseConnections()
