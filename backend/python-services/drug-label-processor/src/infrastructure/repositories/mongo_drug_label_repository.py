from typing import List
from pymongo.collection import Collection
from src.core.entities.drug_label import DrugLabel, ProcessedIndication
from src.infrastructure.interfaces.drug_label_interface import DrugLabelRepository

class MongoDrugLabelRepository(DrugLabelRepository):
    def __init__(self, collection: Collection):
        self.collection = collection
    
    def get_unprocessed_labels(self, limit: int) -> List[DrugLabel]:
        cursor = self.collection.find({"status": "raw"}).limit(limit)
        return [self._document_to_entity(doc) for doc in cursor]
    
    def update_label(self, label: DrugLabel) -> None:
        self.collection.update_one(
            {"_id": label.id},
            {"$set": self._entity_to_document(label)}
        )
    
    def _document_to_entity(self, doc) -> DrugLabel:
        processed_indications = None
        if "processed_indications" in doc:
            processed_indications = [
                ProcessedIndication(
                    original_text=pi["original_text"],
                    icd10_codes=pi["icd10_codes"],
                    mapping_method=pi["mapping_method"]
                )
                for pi in doc["processed_indications"]
            ]
        
        return DrugLabel(
            id=str(doc["_id"]),
            raw_text=doc["raw_text"],
            indications=doc["indications"],
            status=doc["status"],
            processed_at=doc.get("processed_at"),
            processed_indications=processed_indications,
            error=doc.get("error")
        )
    
    def _entity_to_document(self, entity: DrugLabel) -> dict:
        document = {
            "raw_text": entity.raw_text,
            "indications": entity.indications,
            "status": entity.status,
            "processed_at": entity.processed_at,
            "error": entity.error
        }
        
        if entity.processed_indications:
            document["processed_indications"] = [
                {
                    "original_text": pi.original_text,
                    "icd10_codes": pi.icd10_codes,
                    "mapping_method": pi.mapping_method
                }
                for pi in entity.processed_indications
            ]
        
        return document