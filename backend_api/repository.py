# repository.py
# Ansvar: Hantera lagring och logik av Case-objekt
# Just nu används en enkel Lista som "databas"
# Senare: databas (utan att API:t ändras)

from typing import List, Optional
from backend_api.models import Case

""" 
Vad jag lär mig här är att skapa en dedikerad repository-klass för att hantera lagring och hämtning av Case-objekt. Detta abstraherar bort datalagringslogiken från resten av applikationen, vilket gör det enklare att byta ut lagringsmekanismen i framtiden (t.ex. byta från en Lista till en riktig databas) utan att påverka API:t eller domänmodellen. Repository-mönstret hjälper också till att hålla koden organiserad och underlättar enhetstestning genom att isolera datalagringslogiken.
Här tränas:
- objektmutation (uppdatera attribut på ett objekt)
- tydlig retur ('None' om ej hittad)
- framtida DB-tänk
"""

class CaseRepository:
    def __init__(self):
        # Intern lagring (in-memory just nu)
        self._cases: List[Case] = []
        self._next_id: int = 1

    def get_all(self) -> List[Case]:
        return self._cases
    
    def get_by_id(self, case_id: int) -> Optional[Case]:
        return next((c for c in self._cases if c.id == case_id), None)
    
    def create(self, case: Case) -> Case:
        case.id = self._next_id
        self._next_id +=1

        self._cases.append(case)
        return case
    
    def update(self, case_id: int, updated_case) -> Optional[Case]:
        case = self.get_by_id(case_id)
        if case is None:
            return None
        
        case.title = updated_case.title
        case.description = updated_case.description
        case.status = updated_case.status
        return case

    def delete(self, case_id: int) -> bool:
        case = self.get_by_id(case_id)
        if case is None:
            return False
        
        self._cases.remove(case)
        return True
    
