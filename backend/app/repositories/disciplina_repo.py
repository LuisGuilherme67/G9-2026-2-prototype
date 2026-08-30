from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.curso import Curso
from app.models.disciplina import Disciplina, CursoDisciplina, DisciplinaPreRequisito
from app.models.conteudo import Recurso, Dica, Dificuldade, Comentario, AvaliacaoDisciplina, Upvote

class DisciplinaRepository:
    def get_by_slug(self, db: Session, slug: str) -> Optional[Disciplina]:
        return db.query(Disciplina).filter(Disciplina.slug == slug).first()

    def get_with_details(self, db: Session, slug: str) -> Optional[Disciplina]:
        return db.query(Disciplina).options(
            joinedload(Disciplina.requisitos).joinedload(DisciplinaPreRequisito.prerequisite),
            joinedload(Disciplina.recursos),
            joinedload(Disciplina.dicas),
            joinedload(Disciplina.dificuldades),
            joinedload(Disciplina.avaliacoes)
        ).filter(Disciplina.slug == slug).first()

    def list_by_course(self, db: Session, course_slug: str) -> List[Disciplina]:
        return db.query(Disciplina).join(
            CursoDisciplina, CursoDisciplina.subject_id == Disciplina.id
        ).join(
            Curso, Curso.id == CursoDisciplina.course_id
        ).filter(
            Curso.slug == course_slug
        ).order_by(CursoDisciplina.period.asc(), Disciplina.name.asc()).all()

    def get_difficulties_by_subject(self, db: Session, subject_id: int) -> List[Dificuldade]:
        return db.query(Dificuldade).filter(Dificuldade.disciplina_id == subject_id).all()

    def get_tips_by_subject(self, db: Session, subject_id: int) -> List[Dica]:
        return db.query(Dica).filter(Dica.disciplina_id == subject_id).all()

    def get_resources_by_subject(self, db: Session, subject_id: int, category: Optional[str] = None) -> List[Recurso]:
        query = db.query(Recurso).filter(Recurso.disciplina_id == subject_id, Recurso.is_approved.is_(True))
        if category:
            query = query.filter(Recurso.category == category)
        return query.order_by(Recurso.created_at.desc()).all()

    def get_comments(self, db: Session, target_type: str, target_id: int) -> List[Comentario]:
        return db.query(Comentario).filter(
            Comentario.target_type == target_type,
            Comentario.target_id == target_id,
            Comentario.parent_id.is_(None)
        ).order_by(Comentario.created_at.asc()).all()

disciplina_repo = DisciplinaRepository()
