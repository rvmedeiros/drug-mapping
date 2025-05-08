from typing import Optional
from core.entities.drug_indication import DrugIndication
from infrastructure.repositories.drug.drug_repository import DrugRepository
from application.services.scraping.dailymed_scraper_service import DailyMedScraper

class ScrapeDrugUseCase:
    def __init__(self, scraper: DailyMedScraper, repository: DrugRepository):
        self.scraper = scraper
        self.repository = repository
        
    def execute(self, drug_name: str) -> Optional[DrugIndication]:
        scraped_data = self.scraper.get_indications(drug_name)
        if not scraped_data:
            return None
            
        indication = DrugIndication(
            drug_name=scraped_data['drug_name'],
            indications=scraped_data['indications'],
            metadata=scraped_data['metadata']
        )
        
        self.repository.save(indication)
        return indication