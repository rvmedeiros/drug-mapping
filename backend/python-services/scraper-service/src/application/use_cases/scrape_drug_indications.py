from typing import Dict, Optional
from domain.entities.drug_indication import DrugIndication
from domain.repositories.drug_repository import DrugRepository
from infrastructure.scraping.dailymed_scraper import DailyMedScraper

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
            raw_data=scraped_data['raw_data'],
            metadata=scraped_data['metadata']
        )
        
        self.repository.save(indication)
        return indication