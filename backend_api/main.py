# main.py
# Huvudfil för FastAPI-applikationen
# Syfte: Definiera API-endpoints och koppla ihop
# scheman (schemas.py) med domänmodeller (models.py)


from fastapi import FastAPI, HTTPException
from backend_api.schemas import CaseCreate, CaseRead
from backend_api.models import Case
from backend_api.repository import CaseRepository

repo = CaseRepository()  # Skapa repository-instans
app = FastAPI()     # Skapa FastAPI-app


# POST-Endpoint för att skapa ett nytt ärende
# FastAPI tar emot JSON
# Validerar automatiskt med CaseCreate
# Skapa ett Case-objekt (modell)
# Returnerar ett svar enligt CaseRead
# Status code 201 means "Created"
@app.post("/cases/", response_model=CaseRead,  status_code=201) 
def create_case(case: CaseCreate):  # Tar emot validerat schema
    new_case = Case(
        id=0,  # Tillfälligt, sätts i repository
        title=case.title,
        description=case.description,
        status=case.status.value    # <-- Viktigt: Enum till str
    )

    created = repo.create(new_case)
    return CaseRead.model_validate(created)

# Endpoint för att hämta alla ärenden
# Det här är REST-grunden - Collection endpoint
# Returnerar lista ´response_model=list[CaseRead]´
# FastAPI serialiserar objekten till JSON
@app.get("/cases/", response_model=list[CaseRead])
def get_cases():
    return [CaseRead.model_validate(c) for c in repo.get_all()]

# Endpoint för att hämta ett ärende med specifikt id
# Kräver parameter ´case_id´
@app.get("/cases/{case_id}", response_model=CaseRead)
def get_case(case_id: int):
    # returnerar första matchande eller None
    case = repo.get_by_id(case_id)
    # API-kontrakt: 404 om inte hittad
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return CaseRead.model_validate(case)

# Endpoint för att uppdatera ett ärende med specifikt id
@app.put("/cases/{case_id}", response_model=CaseRead)
def update_case(case_id: int, case_update: CaseCreate):
    updated = Case(
        id=case_id,
        title=case_update.title,
        description=case_update.description,
        status=case_update.status.value
    )

    result = repo.update(case_id, updated)
    if result is None:
        raise HTTPException(status_code=404, detail="Case not found")
        
    return CaseRead.model_validate(result)

# Endpoint för att radera ett ärende med specifikt id
# Använder statuskod 204 No Content vid lyckad radering
@app.delete("/cases/{case_id}", status_code=204)
def delete_case(case_id: int):
    deleted = repo.delete(case_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Case not found")