# backend_api\schemas.py
"""
Pydantic schemas for API validation.

Purpose:
- Ensure incoming client data is valid
- Prevent invalid data from reaching the domain layer (models.py)
- Used by FastAPI for request and response validation
"""

from pydantic import BaseModel, ConfigDict, field_validator
# If you want to use Enum types in schemas
from enum import Enum

class CaseStatus(str, Enum):
    open = "open"
    closed = "closed"

# Used when the client sends POST (no id yet)
class CaseCreate(BaseModel):        
    title: str
    description: str
    status: CaseStatus = CaseStatus.open # default value, client can omit status

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

# Used when the API responds (id exists) 
class CaseRead(BaseModel):
    id: int
    title: str
    description: str
    status: CaseStatus

    # It's okay to read values ​​from `object.attribute`
    # not just from dict
    model_config = ConfigDict(from_attributes=True)