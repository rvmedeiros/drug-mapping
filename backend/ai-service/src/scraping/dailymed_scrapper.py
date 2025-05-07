from typing import Any, Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def get_indications(url: str) -> List :
    try:
        _, drug_name = url.split("=")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        WebDriverWait(driver, 30).until(EC.url_changes(url))
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        indication_section = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.drug-label-sections"))
        )
        
        indication_item = _find_indications_item(indication_section)
        if not indication_item:
            print("Could not find 'INDICATIONS AND USAGE' section")
            return {}

        subsections_content = _process_subsections(indication_item)
        
        if not subsections_content:
            print("No valid indications found in subsections")
            return {}


        return {
                "drug_name": drug_name,
                "raw_data": subsections_content,
                "metadata": {
                    "source": "DailyMed",
                    "scraped_at": datetime.now().isoformat(),
                    "version": "1.0"
                },
                "status": "raw" 
               }
                          
    except Exception as e:
        print(f"Error while scraping indications: {str(e)}")
        return {}
    finally:
        if driver:
            driver.quit()

def _find_indications_item(section) -> Any:
    """Helper to locate the INDICATIONS AND USAGE list item"""
    indication_list = section.find_element(By.XPATH, ".//ul")
    list_items = indication_list.find_elements(By.XPATH, ".//li")

    for item in list_items:
        if "INDICATIONS AND USAGE" in item.text:
            return item.find_element(
                By.XPATH, 
                ".//div[contains(@class, 'Section toggle-content closed long-content')]"
            )
    return None

def _process_subsections(section_div) -> List[Dict[str, Any]]:
    """Process all subsections in the indications section with updated field names"""
    sections = []
    
    all_sections = section_div.find_elements(By.XPATH, ".//div[contains(@class, 'Section') and .//h2]")
    
    for section in all_sections:
        section_data = {
            'section_identifier': '',
            'section_header': '',
            'clinical_content': '',
            'usage_restrictions': {}
        }
        
        try:
            h2 = section.find_element(By.XPATH, ".//h2")
            h2 = h2.get_attribute('textContent').strip()
            
            if '\t' in h2:
                section_identifier, section_header  = h2.split('\t')
                section_data['section_identifier'] = section_identifier
                section_data['section_header'] = section_header
            else:
                section_data['section_header'] = h2
                
        except:
            continue
            
        try:
            section_data['clinical_content'] = section.find_element(
                By.XPATH, ".//p[@class='First']").get_attribute('textContent').strip()
        except:
            pass
            
        try:
            for sub in section.find_elements(By.XPATH, ".//div[contains(@class, 'Section')][not(.//h2)]"):                    
                try:
                    limitation_title = sub.find_element(By.XPATH, ".//span[@class='Underline']").get_attribute('textContent').replace(':', '').strip()
                    description =  sub.find_element(By.XPATH, ".//p[not(@class='First')]//span[@class='XmChange']").get_attribute('textContent').strip()                    
                    if 'limitations' in limitation_title.lower():
                        section_data['usage_restrictions'] = {
                            'restriction_type': limitation_title,
                            'description': description
                        }
                except:
                    continue
        except:
            pass
        sections.append(section_data)
        
    return [s for s in sections if s['section_header']]