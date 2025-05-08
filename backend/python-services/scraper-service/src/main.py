from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from api.controller.drug_controller import router as drug_router
from infrastructure.database.databases import get_db, DatabaseConnections
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DatabaseConnections()
    try:
        db.mongo_db.command('ping')
        with db.pg_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT 1')
        db.redis_client.ping()
        app.state.db = db 
        logger.info("✅ All database connections established successfully")
        yield
    finally:
        if hasattr(db, 'pg_conn'):
            db.pg_pool.putconn(db.pg_conn)
        if hasattr(db, 'mongo_client'):
            db.mongo_client.close()
        if hasattr(db, 'redis_client'):
            db.redis_client.close()
        logger.info("🛑 Application shutting down")

app = FastAPI(lifespan=lifespan)
app.include_router(drug_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    async with get_db() as db:
        mongo_ping = db.mongo_db.command('ping')
        
        with db.pg_conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        
        redis_ping = db.redis_client.ping()
        
        return {
            "status": "OK",
            "databases": {
                "mongodb": mongo_ping,
                "postgresql": True,
                "redis": redis_ping
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")