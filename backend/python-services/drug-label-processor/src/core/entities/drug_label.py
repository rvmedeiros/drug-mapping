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
    indications: List[str]
    status: str
    updated_at: Optional[datetime] = None