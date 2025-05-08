from typing import List
from bson import ObjectId
from pymongo.collection import Collection
from core.entities.drug_label import DrugLabel
from infrastructure.interfaces.drug_label_interface import DrugLabelInterface
from datetime import datetime

class MongoDrugRepository(DrugLabelInterface):
    def __init__(self, db, collection_name: str = 'indications'):
        self.collection = db[collection_name]
    
    def get_unprocessed_labels(self, limit: int) -> List[DrugLabel]:
        cursor = self.collection.find({"status": "raw"}).limit(limit)
        return [self._document_to_entity(doc) for doc in cursor]
    
    def update_label(self, label: DrugLabel) -> None:
        update_data = self._entity_to_document(label)
        update_data["updated_at"] = datetime.now()
        update_data["status"] = "processed" 
        
        label_id = ObjectId(label.id) if isinstance(label.id, str) else label.id
        
        result = self.collection.update_one(
            {"_id": label_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            print(f"Failed to update label with id {label.id}")
        else:
            print(f"Successfully updated label with id {label.id}")
    
    def _document_to_entity(self, doc) -> DrugLabel:
        return DrugLabel(
            id=str(doc["_id"]),
            raw_data=doc["raw_data"],
            status=doc["status"],
        )
    
    def _entity_to_document(self, entity: DrugLabel) -> dict:
        return {
            "raw_data": entity.raw_data,
            "status": entity.status,
            "updated_at": entity.updated_at
        }
