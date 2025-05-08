import os
from pymongo import MongoClient
import psycopg2
import psycopg2.pool
import redis
from fastapi import Request
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnections:
    def __init__(self):
        # MongoDB connection
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
        
        # PostgreSQL connection pool
        self.pg_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB_NAME")
        )
        self.pg_conn = self.pg_pool.getconn()
        
        # Redis connection
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            socket_connect_timeout=5
        )

async def get_db(request: Request) -> DatabaseConnections:
    return request.app.state.db
