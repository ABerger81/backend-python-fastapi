# main.py
# Huvudfil för FastAPI-applikationen
# Syfte: Definiera API-endpoints och koppla ihop
# scheman (schemas.py) med domänmodeller (models.py)


from fastapi import FastAPI
from fastapi import HTTPException
from backend_api.schemas import CaseCreate, CaseRead
from backend_api.models import Case
from backend_api.repository import CaseRepository

app = FastAPI()     # Skapa FastAPI-app

repo = CaseRepository()  # Skapa repository-instans


# Endpoint för att skapa ett nytt ärende
# FastAPI tar emot JSON
# Validerar automatiskt med CaseCreate
# Skapa ett Case-objekt (modell)
# Returnerar ett svar enligt CaseRead
@app.post("/cases/", response_model=CaseRead)
def create_case(case: CaseCreate):
    new_case = repo.create(
        title=case.title,
        description=case.description,
        status=case.status
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
    case = repo.get_by_id(case_id)
    # API-kontrakt: 404 om inte hittad
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return CaseRead.model_validate(case)

