from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ProcessedIndication:
    original_text: str
    icd10_codes: List[str]
    mapping_method: str

@dataclass
class DrugLabel:
    id: str
    raw_text: str
    indications: List[str]
    status: str
    processed_at: Optional[datetime] = None
    processed_indications: Optional[List[ProcessedIndication]] = None
    error: Optional[str] = None