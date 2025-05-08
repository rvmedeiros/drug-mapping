from abc import ABC, abstractmethod
from typing import Optional
from core.entities.drug_indication import DrugIndication

class DrugRepository(ABC):
    @abstractmethod
    def save(self, indication: DrugIndication) -> None:
        pass
    
    @abstractmethod
    def get_by_drug_name(self, drug_name: str) -> Optional[DrugIndication]:
        pass