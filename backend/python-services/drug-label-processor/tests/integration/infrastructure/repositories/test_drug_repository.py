import pytest
from unittest.mock import MagicMock
from core.entities.drug_label import DrugLabel
from infrastructure.repositories.mongo_drug_label_repository import MongoDrugLabelRepository

@pytest.fixture
def mock_collection():
    collection = MagicMock()
    cursor_mock = MagicMock()
    cursor_mock.limit.return_value = [{"_id": "1", "raw_text": "test text", "indications": ["ind1", "ind2"], "status": "raw"}]
    collection.find.return_value = cursor_mock
    return collection

@pytest.fixture
def mongo_repository(mock_collection):
    return MongoDrugLabelRepository(mock_collection)

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
