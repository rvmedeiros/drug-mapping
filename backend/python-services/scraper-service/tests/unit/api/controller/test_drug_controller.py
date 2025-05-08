import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.main import app
from src.infrastructure.repositories.drug.drug_repository import DrugRepository
from src.infrastructure.database.databases import DatabaseConnections

client = TestClient(app)

@pytest.fixture
def mock_db():
    db = MagicMock(spec=DatabaseConnections)
    db.mongo_db = MagicMock()
    db.redis_client = MagicMock()
    db.pg_pool = MagicMock()
    return db

@pytest.fixture
def mock_repo():
    return MagicMock(spec=DrugRepository)

@pytest.mark.asyncio
async def test_scrape_drug_function(mock_db, mock_repo):
    from fastapi import BackgroundTasks
    from src.api.controller.drug_controller import scrape_drug
    
    with patch(
        'src.api.controller.drug_controller.get_drug_repository',
        return_value=mock_repo
    ) as mock_get_repo:
        
        mock_background = BackgroundTasks()
        
        result = await scrape_drug(
            background_tasks=mock_background,
            drug_name="aspirin",
            repo=mock_repo
        )
        
        assert result == {
            "status": "success", 
            "message": "Scraping for aspirin started in background!"
        }
        mock_get_repo.assert_not_called()
        assert len(mock_background.tasks) == 1