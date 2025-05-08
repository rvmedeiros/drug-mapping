import time

class MapperService:
    def __init__(self, repository, api_client, interval_seconds=10):
        self.repository = repository
        self.api_client = api_client
        self.interval = interval_seconds

    def run(self):
        while True:
            print("Checking for raw indications...")
            raw_items = self.repository.get_raw_indications()
            if not raw_items:
                print("No raw items found. Waiting...")
            for item in raw_items:
                print(f"Processing {item['_id']}...")
                section_header = item['section_header']
                mapped_codes = self.api_client.map_indication(section_header)
                self.repository.update_indication_status(item['_id'], 'mapped', mapped_codes)
                print(f"Updated {item['_id']} → {mapped_codes}")
            time.sleep(self.interval)