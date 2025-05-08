import pytest
from unittest.mock import Mock, patch
from pymongo.collection import Collection

@pytest.fixture
def mock_collection():
    return Mock(spec=Collection)

@pytest.fixture
def sample_label():
    from core.entities.drug_label import DrugLabel
    return DrugLabel(
        id="1",
        raw_text="sample text",
        indications=["ind1"],
        status="raw"
    )