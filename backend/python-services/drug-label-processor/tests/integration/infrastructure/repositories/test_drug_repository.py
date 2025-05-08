import pytest
from pymongo import MongoClient
from src.infrastructure.database.mongo_database import MongoDrugLabelRepository
from src.core.entities.drug_label import DrugLabel

@pytest.fixture
def mongo_repository(mongo):
    client = MongoClient(mongo)
    db = client["test_db"]
    collection = db["test_collection"]
    collection.delete_many({})
    return MongoDrugLabelRepository(collection)

def test_save_and_retrieve_label(mongo_repository):
    label = DrugLabel(
        id="1",
        raw_text="test text",
        indications=["ind1", "ind2"],
        status="raw"
    )
    
    mongo_repository.update_label(label)
    
    result = mongo_repository.get_unprocessed_labels(limit=1)
    
    assert len(result) == 1
    retrieved = result[0]
    assert retrieved.id == "1"
    assert retrieved.raw_text == "test text"
    assert retrieved.indications == ["ind1", "ind2"]