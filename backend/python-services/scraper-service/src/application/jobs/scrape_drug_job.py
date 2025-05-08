import logging
from infrastructure.scraping.dailymed_scraper import DailyMedScraper
from application.use_cases.scrape_drug_indications import ScrapeDrugUseCase
from domain.repositories.drug_repository import DrugRepository

logger = logging.getLogger(__name__)

def scrape_drug_in_background(drug_name: str, repo: DrugRepository):
    try:
        scraper = DailyMedScraper()
        use_case = ScrapeDrugUseCase(scraper, repo)
        result = use_case.execute(drug_name)
        repo.save(result)

        logger.info(f"Scraping result for {drug_name}: {result}")
    except Exception as e:
        logger.error(f"Error scraping drug '{drug_name}': {e}")
