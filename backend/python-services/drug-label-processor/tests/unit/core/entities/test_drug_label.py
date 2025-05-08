import pytest
from datetime import datetime
from core.entities.drug_label import DrugLabel, ProcessedIndication

def test_create_drug_label():
    indication = ProcessedIndication(
        original_text="atopic dermatitis",
        icd10_codes=["L20"],
        mapping_method="predefined"
    )
    
    label = DrugLabel(
        id="123",
        raw_text="Dupixent label text",
        indications=["atopic dermatitis"],
        status="processed",
        processed_at=datetime.now(),
        processed_indications=[indication]
    )
    
    assert label.id == "123"
    assert len(label.indications) == 1
    assert label.processed_indications[0].icd10_codes == ["L20"]
    assert label.status == "processed"