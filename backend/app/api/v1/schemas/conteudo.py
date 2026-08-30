from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# Dificuldades
class DificuldadeBase(BaseModel):
    topic: str
    description: str

class DificuldadeCreate(DificuldadeBase):
    pass

class DificuldadeResponse(DificuldadeBase):
    id: int
    disciplina_id: int
    user_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Dicas
class DicaBase(BaseModel):
    title: str
    content: str

class DicaCreate(DicaBase):
    pass

class DicaResponse(DicaBase):
    id: int
    disciplina_id: int
    user_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Recursos (Provas, Resumos, etc.)
class RecursoBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str # 'resumo', 'prova', 'link_util', 'extra', 'slide'
    url: str
    semester: Optional[str] = None

class RecursoCreate(RecursoBase):
    pass

class RecursoResponse(RecursoBase):
    id: int
    disciplina_id: int
    user_id: Optional[UUID] = None
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Comentários
class ComentarioCreate(BaseModel):
    target_type: str # 'difficulty', 'tip', 'resource'
    target_id: int
    content: str
    parent_id: Optional[int] = None

class ComentarioResponse(BaseModel):
    id: int
    user_id: UUID
    target_type: str
    target_id: int
    parent_id: Optional[int] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

# Avaliação (Review)
class AvaliacaoCreate(BaseModel):
    difficulty_score: int
    workload_score: int
    status: str # 'aprovado', 'reprovado', 'trancou', 'cursando'
    general_feedback: Optional[str] = None

class AvaliacaoResponse(AvaliacaoCreate):
    id: int
    disciplina_id: int
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Upvote
class UpvoteCreate(BaseModel):
    target_type: str
    target_id: int
