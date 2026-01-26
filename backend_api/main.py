# main.py
# Huvudfil för FastAPI-applikationen
# Syfte: Definiera API-endpoints och koppla ihop
# scheman (schemas.py) med domänmodeller (models.py)


from fastapi import FastAPI
from fastapi import HTTPException
from backend_api.schemas import CaseCreate, CaseRead
from backend_api.models import Case

app = FastAPI()     # Skapa FastAPI-app

# Tillfällig "databas" i minnet
cases: list[Case] = []
current_id = 1


# Endpoint för att skapa ett nytt ärende
# FastAPI tar emot JSON
# Validerar automatiskt med CaseCreate
# Skapa ett Case-objekt (modell)
# Returnerar ett svar enligt CaseRead
@app.post("/cases/", response_model=CaseRead)
def create_case(case: CaseCreate):
    global current_id

    new_case = Case(
        id=current_id,
        title=case.title,
        description=case.description,
        status=case.status
    )

    cases.append(new_case)
    current_id += 1

    return CaseRead.model_validate(new_case)

# Endpoint för att hämta alla ärenden
# Returnerar alla ärenden
# FastAPI serialiserar objekten till JSON
@app.get("/cases/{case_id}", response_model=list[CaseRead])
def get_cases(case_id: int):
    for case in cases:
        if case.id == case_id:
            return CaseRead.model_validate(case)
        
    raise HTTPException(status_code=404, detail="Case not found")

