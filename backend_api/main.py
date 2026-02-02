# main.py
# Huvudfil för FastAPI-applikationen
# Syfte: Definiera API-endpoints och koppla ihop
# scheman (schemas.py) med domänmodeller (models.py)

# Importera FastAPI och HTTPException för felhantering
from fastapi import FastAPI, HTTPException
# Importera Pydantic-scheman
from backend_api.schemas import CaseCreate, CaseRead
# Importera domänmodellen
from backend_api.models import Case
# Importera repository-klassen
from backend_api.repository import CaseRepository
# För Dependency Injection
from fastapi import Depends

app = FastAPI()     # Skapa FastAPI-app
_repo = CaseRepository()
# Dependency Injection-exempel (om vi ville ha det)
# Här skapar vi en funktion som returnerar repository-instansen
# FastAPI kan använda detta för att "injiciera" beroenden
# i endpoints om vi specifierar det i funktionsparametrar
def get_case_repository() -> CaseRepository:
    return _repo

# Endpoint för att skapa ett nytt ärende
# Använder Pydantic-schemat ´CaseCreate´ för indata
# och ´CaseRead´ för utdata
# Status code 201 means "Created"
@app.post("/cases/", response_model=CaseRead,  status_code=201) 
def create_case(
    case_in: CaseCreate,
    repo: CaseRepository = Depends(get_case_repository)
):
    case = repo.create(
        title=case_in.title,
        description=case_in.description,
        status=case_in.status.value
    )
    return CaseRead.model_validate(case)

# Endpoint för att hämta alla ärenden
# Använder Pydantic-schemat ´CaseRead´för utdata
# Returnerar en lista av ärenden
@app.get("/cases/", response_model=list[CaseRead])
def get_cases(
    repo: CaseRepository = Depends(get_case_repository)
):
    return [CaseRead.model_validate(c) for c in repo.get_all()]

# Endpoint för att hämta ett ärende med specifikt id
# Använder Pydantic-schemat ´CaseRead´ för utdata
# Returnerar 404 om ärendet inte finns
@app.get("/cases/{case_id}", response_model=CaseRead)
def get_case(
    case_id: int,
    repo: CaseRepository = Depends(get_case_repository)
):
    # returnerar första matchande eller None
    case = repo.get_by_id(case_id)
    # API-kontrakt: 404 om inte hittad
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return CaseRead.model_validate(case)

# Endpoint för att uppdatera ett ärende med specifikt id
# använder Pydantic-schemat ´CaseCreate´ för indata
# och ´CaseRead´ för utdata
# Returnerar 404 om ärendet inte finns
@app.put("/cases/{case_id}", response_model=CaseRead)
def update_case(
    case_id: int,
    case_update: CaseCreate,
    repo: CaseRepository = Depends(get_case_repository)
):
    case = repo.update(
        case_id,
        title=case_update.title,
        description=case_update.description,
        status=case_update.status.value
    )

    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
        
    return CaseRead.model_validate(case)

# Endpoint för att ta bort ett ärende med specifikt id
# Returnerar 204 No Content vid lyckad borttagning
# Returnerar 404 om ärendet inte finns
@app.delete("/cases/{case_id}", status_code=204)
def delete_case(
    case_id: int,
    repo: CaseRepository = Depends(get_case_repository)
):
    deleted = repo.delete(case_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Case not found")