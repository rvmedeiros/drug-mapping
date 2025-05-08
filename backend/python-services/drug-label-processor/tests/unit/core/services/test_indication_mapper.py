from unittest.mock import Mock
from src.core.services.indication_mapper import IndicationMapper

def test_indication_mapper_interface():
    mapper = Mock(spec=IndicationMapper)
    indication = "atopic dermatitis"
    
    mapper.map_to_icd10.return_value = ["L20"]
    
    result = mapper.map_to_icd10(indication)
    
    assert isinstance(result, list)
    assert all(isinstance(code, str) for code in result)