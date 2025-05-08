import pytest
from unittest.mock import Mock, patch
from pymongo.collection import Collection
from src.infrastructure.mapper.phi2_indication_mapper import Phi2IndicationMapper

@pytest.fixture
def mock_collection():
    return Mock(spec=Collection)

@pytest.fixture
def sample_label():
    from src.core.entities.drug_label import DrugLabel
    return DrugLabel(
        id="1",
        raw_text="sample text",
        indications=["ind1"],
        status="raw"
    )
       
@pytest.fixture
def mock_phi2_mapper():
    with patch('transformers.AutoModelForCausalLM.from_pretrained'), \
         patch('transformers.AutoTokenizer.from_pretrained'):
        mapper = Phi2IndicationMapper()
        mapper._query_llm = Mock(return_value=["L20", "L20.9"])
        return mapper    