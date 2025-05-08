from abc import ABC, abstractmethod
from typing import List

class IndicationMapper(ABC):
    @abstractmethod
    def map_to_icd10(self, indication: str) -> List[str]:
        pass