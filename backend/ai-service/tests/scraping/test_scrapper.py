import pytest
from datetime import datetime
from src.scraping.dailymed_scrapper import get_indications

DAILYMED_URL = "https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=dupixent"

def test_get_indications():
    """Test that the get_indications function returns properly formatted data"""
    indications = get_indications(DAILYMED_URL)
    
    assert indications is not None, "Function should not return None"
    assert isinstance(indications, dict), "Should return a list of drug indications"

    assert 'dupixent' in indications['drug_name'].lower()
    assert 'raw' in indications['status'].lower()
    assert '1.0' in indications['metadata']['version']
    assert len(indications['raw_data']) > 0
    
    
    