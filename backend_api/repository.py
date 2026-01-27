# repository.py
# Ansvar: Hantera lagring och hämntnig av Case-objekt
# Just nu används en enkel lista som "databas"
# Senare: databas (utan att API:t ändras)

from unittest import case
from backend_api.models import Case


class CaseRepository:
    def __init__(self):
        self._cases: list[Case] = []
        self._current_id = 1

    def create(self, title: str, description: str, status: str) -> Case:
        case = Case(
            id=self._current_id,
            title=title,
            description=description,
            status=status
        )
        self._cases.append(case)
        self._current_id += 1
        return case

    def get_all(self) -> list[Case]:
        return self._cases
    
    def get_by_id(self, case_id: int) -> Case | None:
        for case in self._cases:
            if case.id == case_id:
                return case
        return None
    
    """ 
Vad jag lär mig här är att skapa en dedikerad repository-klass för att hantera lagring och hämtning av Case-objekt. Detta abstraherar bort datalagringslogiken från resten av applikationen, vilket gör det enklare att byta ut lagringsmekanismen i framtiden (t.ex. byta från en lista till en riktig databas) utan att påverka API:t eller domänmodellen. Repository-mönstret hjälper också till att hålla koden organiserad och underlättar enhetstestning genom att isolera datalagringslogiken.
 """
    
    def update(self, case_id: int, title: str, description: str, status: str) -> Case | None:
        case = self.get_by_id(case_id)
        if case is None:
            return None
        
        case.title = title
        case.description = description
        case.status = status
        return case

"""
Här tränas:
- objektmutation (uppdatera attribut på ett objekt)
- tydlig retur (´None´ om ej hittad)
- framtida DB-tänk
"""
