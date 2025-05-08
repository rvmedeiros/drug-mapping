import pytest
from unittest.mock import MagicMock
from application.services.mapper_service import MapperService

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_api_client():
    return MagicMock()

@pytest.fixture
def mapper_service(mock_repository, mock_api_client):
    return MapperService(mock_repository, mock_api_client, interval_seconds=0)

def test_mapper_service_processes_raw_indications(mapper_service, mock_repository, mock_api_client):
    raw_item = {'_id': 'abc123', 'section_header': 'Asthma'}
    mock_repository.get_raw_indications.return_value = [raw_item]
    mock_api_client.map_indication.return_value = ['J45']

    mapper_service.repository.get_raw_indications()
    for item in mock_repository.get_raw_indications.return_value:
        section_header = item['section_header']
        mapped_codes = mapper_service.api_client.map_indication(section_header)
        mapper_service.repository.update_indication_status(item['_id'], 'mapped', mapped_codes)

    mock_repository.get_raw_indications.assert_called_once()
    mock_api_client.map_indication.assert_called_once_with('Asthma')
    mock_repository.update_indication_status.assert_called_once_with('abc123', 'mapped', ['J45'])
