from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.analytics_svc import analytics_service
from app.api.v1.schemas.analytics import SubjectAnalyticsResponse, CursoAnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["Analytics & Estatísticas"])

@router.get("/disciplina/{slug}", response_model=SubjectAnalyticsResponse)
def obter_metricas_disciplina(
    slug: str,
    course_id: Optional[int] = Query(None, description="Filtrar por curso específico"),
    db: Session = Depends(get_db)
):
    dados = analytics_service.get_subject_metrics(db, slug, course_id)
    if not dados:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada ou sem dados analíticos.")
    return dados

@router.get("/curso/{course_id}", response_model=List[CursoAnalyticsResponse])
def obter_metricas_curso(
    course_id: int,
    db: Session = Depends(get_db)
):
    return analytics_service.get_course_analytics(db, course_id)
