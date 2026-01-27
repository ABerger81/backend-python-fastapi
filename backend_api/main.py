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
@app.post("/cases/", response_model=CaseRead)
def create_case(case_in: CaseCreate):  # Tar emot validerat schema
    new_case = repo.create(
        title=case_in.title,
        description=case_in.description,
        status=case_in.status.value    # <-- Viktigt: Enum till str
    )
    return CaseRead.model_validate(new_case)

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
    updated_case = repo.update(
        case_id=case_id,
        title=case_update.title,
        description=case_update.description,
        status=case_update.status.value
    )
    if updated_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
        
    return CaseRead.model_validate(updated_case)

# Endpoint för att radera ett ärende med specifikt id
# Använder statuskod 204 No Content vid lyckad radering
@app.delete("/cases/{case_id}", status_code=204)
def delete_case(case_id: int):
    deleted = repo.delete(case_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Case not found")