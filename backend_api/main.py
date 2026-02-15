# backend_api\main.py
"""
# FastAPI application entry point.

Responsibilities:
- Define HTTP endpoints
- Handle HTTP-specific concerns (status codes, errors)
- Delegate business logic to services
"""

from fastapi import FastAPI, HTTPException, Depends, Response
from backend_api.dependencies import get_case_service
from backend_api.schemas import CaseCreate, CaseRead
from backend_api.services.case_service import CaseService

app = FastAPI()


@app.post("/cases/", status_code=201, response_model=CaseRead)
def create_case(
    payload: CaseCreate,
    service: CaseService = Depends(get_case_service),
):
    try:
        case = service.create_case(
            title=payload.title,
            description=payload.description,
            status=payload.status.value,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CaseRead.model_validate(case)


@app.get("/cases/", response_model=list[CaseRead])
def get_cases(
    service: CaseService = Depends(get_case_service),
):
    cases = service.get_all_cases()
    return [CaseRead.model_validate(c) for c in cases]


@app.get("/cases/{case_id}", response_model=CaseRead)
def get_case(
    case_id: int,
    service: CaseService = Depends(get_case_service),
):
    case = service.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return CaseRead.model_validate(case)


@app.put("/cases/{case_id}", response_model=CaseRead)
def update_case(
    case_id: int,
    payload: CaseCreate,
    service: CaseService = Depends(get_case_service),
):
    try:
        case = service.update_case(
            case_id,
            title=payload.title,
            description=payload.description,
            status=payload.status.value,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    return CaseRead.model_validate(case)


@app.delete("/cases/{case_id}", status_code=204)
def delete_case(
    case_id: int,
    service: CaseService = Depends(get_case_service),
):
    deleted = service.delete_case(case_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Case not found")

    return Response(status_code=204)