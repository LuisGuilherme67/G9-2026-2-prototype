from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.disciplina_repo import disciplina_repo
from app.models.conteudo import Dificuldade, Dica, Recurso, Comentario, AvaliacaoDisciplina, Upvote
from app.domain.moderation import verificar_conteudo_apropriado, sanitizar_texto

class CadeiraService:
    def get_cadeira_hub(self, db: Session, slug: str) -> Optional[Dict[str, Any]]:
        disciplina = disciplina_repo.get_with_details(db, slug)
        if not disciplina:
            return None

        # Formata pré-requisitos
        prerequisitos = [
            {
                "id": req.prerequisite.id,
                "name": req.prerequisite.name,
                "code": req.prerequisite.code,
                "slug": req.prerequisite.slug
            }
            for req in disciplina.requisitos if req.prerequisite
        ]

        # Média de avaliações dos estudantes
        avaliacoes = disciplina.avaliacoes or []
        total_avaliacoes = len(avaliacoes)
        media_dificuldade = (
            round(sum(a.difficulty_score for a in avaliacoes) / total_avaliacoes, 1)
            if total_avaliacoes > 0 else None
        )
        media_trabalho = (
            round(sum(a.workload_score for a in avaliacoes) / total_avaliacoes, 1)
            if total_avaliacoes > 0 else None
        )

        return {
            "id": disciplina.id,
            "name": disciplina.name,
            "code": disciplina.code,
            "slug": disciplina.slug,
            "description": disciplina.description,
            "workload_hours": disciplina.workload_hours,
            "credits": disciplina.credits,
            "department": disciplina.department,
            "prerequisites": prerequisitos,
            "community_stats": {
                "total_reviews": total_avaliacoes,
                "average_difficulty": media_dificuldade,
                "average_workload": media_trabalho
            }
        }

    def add_comment(
        self, db: Session, user_id: Any, target_type: str, target_id: int, content: str, parent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Valida com moderação ética e cria comentário."""
        content_clean = sanitizar_texto(content)
        is_valido, erros = verificar_conteudo_apropriado(content_clean)
        
        if not is_valido:
            raise ValueError(f"Comentário rejeitado pelas regras da comunidade: {', '.join(erros)}")

        comentario = Comentario(
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            parent_id=parent_id,
            content=content_clean
        )
        db.add(comentario)
        db.commit()
        db.refresh(comentario)

        return {
            "id": comentario.id,
            "user_id": str(comentario.user_id),
            "target_type": comentario.target_type,
            "target_id": comentario.target_id,
            "parent_id": comentario.parent_id,
            "content": comentario.content,
            "created_at": comentario.created_at
        }

cadeira_service = CadeiraService()
