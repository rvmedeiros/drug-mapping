from typing import List, Dict, Optional
from groq import AsyncGroq
import asyncio
import os
from dotenv import load_dotenv
from src.core.services.indication_mapper import IndicationMapper


class Phi2IndicationMapper(IndicationMapper):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = AsyncGroq(api_key=api_key)
        self.model = "llama3-70b-8192"
        self._setup_predefined_mappings()
        self.system_prompt = """
        Return ONLY comma-separated ICD-10 codes for medical conditions.
        If unknown, return UNMAPPABLE.
        """

    def _setup_predefined_mappings(self) -> None:
        self.predefined_mappings = {
            "atopic dermatitis": ["L20"],
            "asthma": ["J45"],
            "chronic rhinosinusitis": ["J32"],
            "severe atopic dermatitis": ["L20", "L20.9"],
            "high blood pressure": ["I10"],
            "hypertension": ["I10"]
        }

    def _get_predefined_mapping(self, indication: str) -> Optional[List[str]]:
        return self.predefined_mappings.get(indication.lower())

    async def _query_groq(self, indication: str) -> List[str]:
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user", 
                        "content": f"Condition: {indication}\nICD-10 Codes:"
                    }
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=50,
                stop=["\n"]
            )
            
            response = chat_completion.choices[0].message.content
            return self._parse_response(response)
        except Exception as e:
            print(f"Error querying Groq: {e}")
            return ["UNMAPPABLE"]

    def _parse_response(self, response: str) -> List[str]:
        codes = [code.strip() for code in response.split(',') if code.strip()]
        return codes if codes else ["UNMAPPABLE"]

    async def map_to_icd10_async(self, indication: str) -> List[str]:
        if not indication:
            return ["UNMAPPABLE"]
        predefined = self._get_predefined_mapping(indication)
        if predefined:
            return predefined
        return await self._query_groq(indication)

    # Versão síncrona wrapper para compatibilidade
    def map_to_icd10(self, indication: str) -> List[str]:
        return asyncio.run(self.map_to_icd10_async(indication))