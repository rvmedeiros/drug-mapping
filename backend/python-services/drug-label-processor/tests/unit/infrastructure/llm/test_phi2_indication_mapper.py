import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.llm.phi2_indication_mapper import Phi2IndicationMapper

@pytest.fixture
def mapper():
    with patch('transformers.AutoModelForCausalLM.from_pretrained'), \
         patch('transformers.AutoTokenizer.from_pretrained'):
        return Phi2IndicationMapper()

def test_map_known_indication(mapper):
    with patch.object(mapper, '_get_predefined_mapping', return_value=["L20"]):
        result = mapper.map_to_icd10("atopic dermatitis")
        assert result == ["L20"]

def test_map_unknown_indication(mapper):
    with patch.object(mapper, '_get_predefined_mapping', return_value=None), \
         patch.object(mapper, '_query_llm', return_value=["L20", "L20.9"]):
        result = mapper.map_to_icd10("severe atopic dermatitis")
        assert result == ["L20", "L20.9"]

def test_llm_query_formatting(mapper):
    with patch.object(mapper, '_get_predefined_mapping', return_value=None), \
         patch.object(mapper.model, 'generate') as mock_generate:
        mock_generate.return_value = MagicMock()
        mapper.tokenizer.batch_decode.return_value = ["Output: L20"]
        
        mapper.map_to_icd10("atopic dermatitis")
        
        args, _ = mapper.tokenizer.call_args
        assert "atopic dermatitis" in args[0]
        assert "ICD-10 codes" in args[0]