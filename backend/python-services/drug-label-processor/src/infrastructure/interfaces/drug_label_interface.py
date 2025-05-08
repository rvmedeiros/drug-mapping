from abc import ABC, abstractmethod
from typing import List
from core.entities.drug_label import DrugLabel

class DrugLabelInterface(ABC):
    @abstractmethod
    def get_unprocessed_labels(self, limit: int) -> List[DrugLabel]:
        """Retrieve unprocessed drug labels from the repository"""
        pass
    
    @abstractmethod
    def update_label(self, label: DrugLabel) -> None:
        """Update a drug label in the repository"""
        pass