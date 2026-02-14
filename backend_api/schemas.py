# backend_api\schemas.py
"""
Pydantic-schema (validering och API)
Syfte: Säkerställa att data från användaren är korrekt
innan dn når logiken (models.py) i systemet.
FastAPI använder dessa scheman för att validera
inkommande och utgående data.
"""

from pydantic import BaseModel, ConfigDict
# Om du vill använda Enum-typer i scheman
from enum import Enum

class CaseStatus(str, Enum):
    open = "open"
    closed = "closed"

# Används när klienten skickar POST (inget id ännu)
class CaseCreate(BaseModel):        
    title: str
    description: str
    status: CaseStatus = CaseStatus.open # defaultvärde, klienten kan utelämna status

# Används när API:t svarar (id finns)
class CaseRead(BaseModel):
    id: int
    title: str
    description: str
    status: CaseStatus

    # Det är okej att läsa värden från `objekt.attribut`
    # inte bara från dict
    model_config = ConfigDict(from_attributes=True)