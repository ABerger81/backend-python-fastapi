# schemas.py
# Pydantic-schema (validering och API)
# Syfte: Säkerställa att data från användaren är korrekt
# innan dn når logiken (models.py) i systemet.
# FastAPI använder dessa scheman för att validera
# inkommande och utgående data.


from pydantic import BaseModel, ConfigDict

# Används när klienten skickar POST (inget id ännu)
class CaseCreate(BaseModel):        
    title: str
    description: str
    status: str

# Används när API:t svarar (id finns)
class CaseRead(BaseModel):
    id: int
    title: str
    description: str
    status: str

    # Det är okej att läsa värden från `objekt.attribut`
    # inte bara från dict
    model_config = ConfigDict(from_attributes=True)