from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, get_current_active_user_required
from app.models.curso import Curso
from app.models.disciplina import Disciplina
from app.models.conteudo import Dificuldade, Dica, Recurso, Comentario, AvaliacaoDisciplina, Upvote, User
from app.repositories.disciplina_repo import disciplina_repo
from app.services.cadeira_svc import cadeira_service
from app.api.v1.schemas.curso import CursoResponse
from app.api.v1.schemas.disciplina import DisciplinaResponse, DisciplinaHubResponse
from app.api.v1.schemas.conteudo import (
    DificuldadeCreate, DificuldadeResponse,
    DicaCreate, DicaResponse,
    RecursoCreate, RecursoResponse,
    ComentarioCreate, ComentarioResponse,
    AvaliacaoCreate, AvaliacaoResponse,
    UpvoteCreate
)

router = APIRouter(tags=["Cadeiras e Cursos"])

# ----------------- CURSOS -----------------
@router.get("/cursos", response_model=List[CursoResponse])
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(Curso).order_by(Curso.name.asc()).all()

# ----------------- DISCIPLINAS / CADEIRAS -----------------
@router.get("/cadeiras", response_model=List[DisciplinaResponse])
def listar_cadeiras(
    curso_slug: Optional[str] = Query(None, description="Filtrar por slug do curso (ex: ciencia-da-computacao)"),
    search: Optional[str] = Query(None, description="Termo de busca no nome da matéria"),
    db: Session = Depends(get_db)
):
    if curso_slug:
        return disciplina_repo.list_by_course(db, curso_slug)
    
    query = db.query(Disciplina)
    if search:
        query = query.filter(Disciplina.name.ilike(f"%{search}%"))
    return query.order_by(Disciplina.name.asc()).all()

@router.get("/cadeiras/{slug}", response_model=DisciplinaHubResponse)
def obter_detalhes_cadeira(slug: str, db: Session = Depends(get_db)):
    hub_data = cadeira_service.get_cadeira_hub(db, slug)
    if not hub_data:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    return hub_data

# ----------------- DIFICULDADES COMUNS -----------------
@router.get("/cadeiras/{slug}/dificuldades", response_model=List[DificuldadeResponse])
def listar_dificuldades_cadeira(slug: str, db: Session = Depends(get_db)):
    disciplina = disciplina_repo.get_by_slug(db, slug)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    return disciplina_repo.get_difficulties_by_subject(db, disciplina.id)

@router.post("/cadeiras/{slug}/dificuldades", response_model=DificuldadeResponse, status_code=status.HTTP_201_CREATED)
def criar_dificuldade(
    slug: str,
    dif_in: DificuldadeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_required)
):
    disciplina = disciplina_repo.get_by_slug(db, slug)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    
    dif = Dificuldade(
        disciplina_id=disciplina.id,
        user_id=current_user.id,
        topic=dif_in.topic,
        description=dif_in.description
    )
    db.add(dif)
    db.commit()
    db.refresh(dif)
    return dif

# ----------------- DICAS & CONSELHOS -----------------
@router.get("/cadeiras/{slug}/dicas", response_model=List[DicaResponse])
def listar_dicas_cadeira(slug: str, db: Session = Depends(get_db)):
    disciplina = disciplina_repo.get_by_slug(db, slug)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    return disciplina_repo.get_tips_by_subject(db, disciplina.id)

@router.post("/cadeiras/{slug}/dicas", response_model=DicaResponse, status_code=status.HTTP_201_CREATED)
def criar_dica(
    slug: str,
    dica_in: DicaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_required)
):
    disciplina = disciplina_repo.get_by_slug(db, slug)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    
    dica = Dica(
        disciplina_id=disciplina.id,
        user_id=current_user.id,
        title=dica_in.title,
        content=dica_in.content
    )
    db.add(dica)
    db.commit()
    db.refresh(dica)
    return dica

# ----------------- MATERIAIS & PROVAS ANTIGAS -----------------
@router.get("/cadeiras/{slug}/recursos", response_model=List[RecursoResponse])
def listar_recursos_cadeira(
    slug: str,
    category: Optional[str] = Query(None, description="Filtrar por categoria: prova, resumo, link_util, extra, slide"),
    db: Session = Depends(get_db)
):
    disciplina = disciplina_repo.get_by_slug(db, slug)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    return disciplina_repo.get_resources_by_subject(db, disciplina.id, category)

@router.post("/cadeiras/{slug}/recursos", response_model=RecursoResponse, status_code=status.HTTP_201_CREATED)
def adicionar_recurso(
    slug: str,
    rec_in: RecursoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_required)
):
    disciplina = disciplina_repo.get_by_slug(db, slug)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    
    recurso = Recurso(
        disciplina_id=disciplina.id,
        user_id=current_user.id,
        title=rec_in.title,
        description=rec_in.description,
        category=rec_in.category,
        url=rec_in.url,
        semester=rec_in.semester
    )
    db.add(recurso)
    db.commit()
    db.refresh(recurso)
    return recurso

# ----------------- COMENTÁRIOS E DISCUSSÕES -----------------
@router.get("/comentarios", response_model=List[ComentarioResponse])
def listar_comentarios(
    target_type: str = Query(..., description="Tipo do alvo: difficulty, tip, resource"),
    target_id: int = Query(..., description="ID do alvo"),
    db: Session = Depends(get_db)
):
    return disciplina_repo.get_comments(db, target_type, target_id)

@router.post("/comentarios", response_model=ComentarioResponse, status_code=status.HTTP_201_CREATED)
def postar_comentario(
    comentario_in: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_required)
):
    try:
        return cadeira_service.add_comment(
            db,
            user_id=current_user.id,
            target_type=comentario_in.target_type,
            target_id=comentario_in.target_id,
            content=comentario_in.content,
            parent_id=comentario_in.parent_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------- AVALIAÇÕES (REVIEWS) -----------------
@router.post("/cadeiras/{slug}/avaliacoes", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def avaliar_cadeira(
    slug: str,
    review_in: AvaliacaoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_required)
):
    disciplina = disciplina_repo.get_by_slug(db, slug)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada.")
    
    # Verifica se já avaliou
    existing = db.query(AvaliacaoDisciplina).filter(
        AvaliacaoDisciplina.disciplina_id == disciplina.id,
        AvaliacaoDisciplina.user_id == current_user.id
    ).first()
    
    if existing:
        existing.difficulty_score = review_in.difficulty_score
        existing.workload_score = review_in.workload_score
        existing.status = review_in.status
        existing.general_feedback = review_in.general_feedback
        db.commit()
        db.refresh(existing)
        return existing

    review = AvaliacaoDisciplina(
        disciplina_id=disciplina.id,
        user_id=current_user.id,
        difficulty_score=review_in.difficulty_score,
        workload_score=review_in.workload_score,
        status=review_in.status,
        general_feedback=review_in.general_feedback
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

# ----------------- UPVOTES -----------------
@router.post("/upvotes", status_code=status.HTTP_200_OK)
def toggle_upvote(
    upvote_in: UpvoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_required)
):
    existing = db.query(Upvote).filter(
        Upvote.user_id == current_user.id,
        Upvote.target_type == upvote_in.target_type,
        Upvote.target_id == upvote_in.target_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"voted": False, "message": "Upvote removido."}
    
    new_upvote = Upvote(
        user_id=current_user.id,
        target_type=upvote_in.target_type,
        target_id=upvote_in.target_id
    )
    db.add(new_upvote)
    db.commit()
    return {"voted": True, "message": "Upvote adicionado com sucesso."}
