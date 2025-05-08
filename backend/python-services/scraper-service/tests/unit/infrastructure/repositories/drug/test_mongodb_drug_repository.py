import pytest
from domain.entities.drug_indication import DrugIndication
from infrastructure.repositories.drug.repositories import MongoDBDrugRepository
from datetime import datetime, timezone, timedelta

import mongomock

@pytest.fixture
def mock_mongo_db():
    client = mongomock.MongoClient()
    db = client.test_database
    yield db

@pytest.fixture
def drug_indication():
    return DrugIndication(
        drug_name="Aspirin",
        raw_data="Some raw data",
        metadata={"key": "value"},
        status="approved",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

@pytest.fixture
def repository(mock_mongo_db):
    return MongoDBDrugRepository(mock_mongo_db)

def test_save_creates_or_updates_drug_indication(repository, drug_indication, mock_mongo_db):
    result = repository.save(drug_indication)

    collection = mock_mongo_db["indications"]
    saved_data = collection.find_one({"drug_name": drug_indication.drug_name})

    assert saved_data["drug_name"] == drug_indication.drug_name
    assert saved_data["raw_data"] == drug_indication.raw_data
    assert saved_data["metadata"] == drug_indication.metadata
    assert saved_data["status"] == drug_indication.status
    assert "created_at" in saved_data
    assert "updated_at" in saved_data

def test_get_by_drug_name_returns_drug_indication(repository, drug_indication, mock_mongo_db):
    repository.save(drug_indication)
    result = repository.get_by_drug_name(drug_indication.drug_name)

    assert result is not None
    assert result.drug_name == drug_indication.drug_name
    assert result.raw_data == drug_indication.raw_data
    assert result.metadata == drug_indication.metadata
    assert result.status == drug_indication.status
    assert result.created_at is not None
    assert result.updated_at is not None

def test_get_by_drug_name_returns_none_if_not_found(repository, mock_mongo_db):
    result = repository.get_by_drug_name("NonExistentDrug")
    assert result is None
