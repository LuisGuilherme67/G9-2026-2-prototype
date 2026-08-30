from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CursoBase(BaseModel):
    name: str
    code: Optional[str] = None
    slug: str
    department: Optional[str] = None
    description: Optional[str] = None

class CursoCreate(CursoBase):
    pass

class CursoResponse(CursoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
