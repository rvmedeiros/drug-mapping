import pytest
from src.application.services.ai_agent_service import Phi2IndicationMapper

@pytest.fixture(scope="module")
def mapper():
    return Phi2IndicationMapper()

@pytest.mark.integration
def test_known_indication_mapping(mapper):
    result = mapper.map_to_icd10("atopic dermatitis")
    assert "L20" in result
    assert isinstance(result, list)

@pytest.mark.integration
def test_unknown_indication_mapping(mapper):
    result = mapper.map_to_icd10("severe refractory atopic dermatitis")
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0] != "UNMAPPABLE"

@pytest.mark.asyncio
async def test_async_mapping():
    mapper = Phi2IndicationMapper()
    result = await mapper.map_to_icd10_async("asthma")
    assert "J45" in result