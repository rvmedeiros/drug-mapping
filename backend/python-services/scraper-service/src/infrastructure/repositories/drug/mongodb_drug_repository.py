from datetime import datetime, timezone
from typing import Optional
from pymongo.database import Database
from core.entities.drug_indication import DrugIndication
from infrastructure.repositories.drug.drug_repository import DrugRepository

class MongoDBDrugRepository(DrugRepository):
    def __init__(self, mongo_db: Database):
        self.collection = mongo_db["indications"]
    
    def save(self, indication: DrugIndication) -> str:
        data = {
            "drug_name": indication.drug_name,
            "indications": indication.indications,
            "metadata": indication.metadata,
            "status": indication.status,
            "created_at": indication.created_at,
            "updated_at": datetime.now(timezone.utc)
        }
        
        result = self.collection.update_one(
            {"drug_name": indication.drug_name},
            {"$set": data},
            upsert=True
        )
        
        return f"Matched: {result.matched_count}, Modified: {result.modified_count}"

    def get_by_drug_name(self, drug_name: str) -> Optional[DrugIndication]:
        data = self.collection.find_one(
            {"drug_name": drug_name},
            projection={"_id": False}
        )
        return DrugIndication(**data) if data else None