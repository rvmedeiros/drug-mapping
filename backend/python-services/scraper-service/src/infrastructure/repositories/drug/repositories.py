from fastapi import Depends
from pymongo.database import Database
from infrastructure.database.databases import get_db
from infrastructure.repositories.drug.drug_repository import DrugRepository
from infrastructure.repositories.drug.mongodb_drug_repository import MongoDBDrugRepository

async def get_drug_repository(db = Depends(get_db)) -> DrugRepository:
    if not hasattr(db, 'mongo_db'):
        raise RuntimeError("MongoDB connection is not available")
    return MongoDBDrugRepository(db.mongo_db)