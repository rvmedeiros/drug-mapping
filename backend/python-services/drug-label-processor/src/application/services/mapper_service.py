import time
from datetime import datetime

class MapperService:
    def __init__(self, repository, phi2IndicationMapper, interval_seconds=10):
        self.repository = repository
        self.interval = interval_seconds
        self.phi2IndicationMapper = phi2IndicationMapper

    def run(self):
        while True:
            print("Checking for raw indications...")
            labels = self.repository.get_unprocessed_labels(1)
            
            for label in labels:
                if not label.indications:
                    print("No raw items found. Waiting...")
                for item in label.indications:
                    if not label.indications:
                        print("No raw items found. Waiting...")
                        continue
                
                    section_header = item['section_header']
                    mapped_codes = self.phi2IndicationMapper.map_to_icd10(section_header)
                    item['icd10_codes'] = mapped_codes
     
                self.repository.update_label(label)
                
                