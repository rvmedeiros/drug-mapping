import os
from dotenv import load_dotenv
from typing import Dict, List, Any
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime

load_dotenv()
DAILYMED_URL = os.getenv("DAILYMED_URL")


class DailyMedScraper:
    def get_indications(self, drug_name: str) -> Any:
        url = f"{DAILYMED_URL}/search.cfm?query={drug_name}"
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
                page = browser.new_page()
                page.goto(url, timeout=30000)

                page.wait_for_load_state("networkidle", timeout=30000)
                page.wait_for_selector("body", timeout=30000)
                page.wait_for_selector("div.drug-label-sections", timeout=30000)

                indication_section = page.query_selector("div.drug-label-sections")

                indication_item = self._find_indications_item(indication_section)
                if not indication_item:
                    print("Could not find 'INDICATIONS AND USAGE' section")
                    return None

                subsections_content = self._process_subsections(indication_item)

                if not subsections_content:
                    print("No valid indications found in subsections")
                    return None

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

        except PlaywrightTimeoutError as e:
            print(f"Timeout while scraping indications: {str(e)}")
            return None
        except Exception as e:
            print(f"Error while scraping indications: {str(e)}")
            return None

    def _find_indications_item(self, section) -> Any:
        """Helper to locate the INDICATIONS AND USAGE list item"""
        indication_list = section.query_selector("ul")
        list_items = indication_list.query_selector_all("li")

        for item in list_items:
            text = item.inner_text()
            if "INDICATIONS AND USAGE" in text:
                return item.query_selector(
                    "div.Section.toggle-content.closed.long-content"
                )
        return None

    def _process_subsections(self, section_div) -> List[Dict[str, Any]]:
        """Process all subsections in the indications section with updated field names"""
        sections = []

        all_sections = section_div.query_selector_all("div.Section:has(h2)")

        for section in all_sections:
            section_data = {
                'section_identifier': '',
                'section_header': '',
                'clinical_content': '',
                'usage_restrictions': {}
            }

            try:
                h2 = section.query_selector("h2").inner_text().strip()
                if '\t' in h2:
                    section_identifier, section_header = h2.split('\t')
                    section_data['section_identifier'] = section_identifier
                    section_data['section_header'] = section_header
                else:
                    section_data['section_header'] = h2
            except:
                continue

            try:
                first_p = section.query_selector("p.First")
                if first_p:
                    section_data['clinical_content'] = first_p.inner_text().strip()
            except:
                pass

            try:
                subs = section.query_selector_all("div.Section:not(:has(h2))")
                for sub in subs:
                    try:
                        limitation_title = sub.query_selector("span.Underline").inner_text().replace(':', '').strip()
                        description = sub.query_selector("p:not(.First) span.XmChange").inner_text().strip()
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
