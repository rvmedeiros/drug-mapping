from dotenv import load_dotenv
from infrastructure.scraping.dailymed_scraper import DailyMedScraper

load_dotenv()

DRUG_NAME = "dupixent"

def test_get_indications():
    """Test that the get_indications function returns properly formatted data"""
    scraper = DailyMedScraper()
    indications = scraper.get_indications(DRUG_NAME)
    
    assert indications is not None, "Function should not return None"
    assert isinstance(indications, dict), "Should return a list of drug indications"

    assert 'dupixent' in indications['drug_name'].lower()
    assert 'raw' in indications['status'].lower()
    assert '1.0' in indications['metadata']['version']
    assert len(indications['raw_data']) > 0