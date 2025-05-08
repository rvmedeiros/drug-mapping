import logging
from fastapi import APIRouter, Depends, Query, BackgroundTasks
from domain.repositories.drug_repository import DrugRepository
from infrastructure.repositories.drug.repositories import get_drug_repository
from application.jobs.scrape_drug_job import scrape_drug_in_background 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/scraper/")
async def scrape_drug(
    background_tasks: BackgroundTasks,
    drug_name: str = Query(..., description="The drug name or search term"),
    repo: DrugRepository = Depends(get_drug_repository)
):
    background_tasks.add_task(scrape_drug_in_background, drug_name, repo)
    return {"status": "success", "message": f"Scraping for {drug_name} started in background!"}