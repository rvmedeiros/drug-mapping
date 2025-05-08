from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Dict, Optional

@dataclass
class DrugIndication:
    drug_name: str
    raw_data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    status: str = "raw"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    

    def mark_as_processed(self):
        self.status = "processed"
        
    def add_icd10_mapping(self, codes: List[str]):
        if not hasattr(self, 'icd10_codes'):
            self.icd10_codes = []
        self.icd10_codes.extend(codes)
        self.status = "mapped"