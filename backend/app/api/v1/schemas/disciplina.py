from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PreRequisitoItem(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    slug: str

    class Config:
        from_attributes = True

class DisciplinaBase(BaseModel):
    name: str
    code: Optional[str] = None
    slug: str
    description: Optional[str] = None
    workload_hours: Optional[int] = None
    credits: Optional[int] = None
    department: Optional[str] = None

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaResponse(DisciplinaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CommunityStats(BaseModel):
    total_reviews: int = 0
    average_difficulty: Optional[float] = None
    average_workload: Optional[float] = None

class DisciplinaHubResponse(DisciplinaBase):
    id: int
    prerequisites: List[PreRequisitoItem] = []
    community_stats: CommunityStats

    class Config:
        from_attributes = True
