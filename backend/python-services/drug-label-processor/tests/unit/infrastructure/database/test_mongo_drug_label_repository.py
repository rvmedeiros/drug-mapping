import pytest
from unittest.mock import Mock, patch
from pymongo.collection import Collection
from datetime import datetime
from src.core.entities.drug_label import DrugLabel, ProcessedIndication
from src.infrastructure.database.mongo_database import MongoDrugLabelRepository

@pytest.fixture
def mock_collection():
    collection = Mock(spec=Collection)    
    mock_cursor = Mock()
    mock_cursor.limit.return_value = [
        {
            "_id": "1",
            "raw_text": "text1",
            "indications": ["ind1"],
            "status": "raw"
        },
        {
            "_id": "2",
            "raw_text": "text2",
            "indications": ["ind2"],
            "status": "raw"
        }
    ]
    
    collection.find.return_value = mock_cursor
    return collection

@pytest.fixture
def repository(mock_collection):
    return MongoDrugLabelRepository(mock_collection)

def test_get_unprocessed_labels(repository, mock_collection):
    result = repository.get_unprocessed_labels(limit=2)
    
    assert len(result) == 2
    assert result[0].id == "1"
    assert result[1].indications == ["ind2"]
    mock_collection.find.assert_called_once_with({"status": "raw"})
    mock_collection.find.return_value.limit.assert_called_once_with(2)

def test_update_label(repository, mock_collection):
    processed_at = datetime.now()
    indication = ProcessedIndication(
        original_text="ind1",
        icd10_codes=["L20"],
        mapping_method="predefined"
    )
    label = DrugLabel(
        id="1",
        raw_text="text1",
        indications=["ind1"],
        status="processed",
        processed_at=processed_at,
        processed_indications=[indication]
    )
    
    repository.update_label(label)
    
    mock_collection.update_one.assert_called_once_with(
        {"_id": "1"},
        {"$set": {
            "raw_text": "text1",
            "indications": ["ind1"],
            "status": "processed",
            "processed_at": processed_at,
            "processed_indications": [{
                "original_text": "ind1",
                "icd10_codes": ["L20"],
                "mapping_method": "predefined"
            }],
            "error": None
        }}
    )