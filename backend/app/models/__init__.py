from app.core.database import Base
from app.models.curso import Curso
from app.models.disciplina import Disciplina, CursoDisciplina, DisciplinaPreRequisito
from app.models.metrica import MetricaDesempenho, EstatisticaCurso
from app.models.conteudo import (
    User,
    Recurso,
    Dica,
    Dificuldade,
    Comentario,
    AvaliacaoDisciplina,
    Upvote
)

__all__ = [
    "Base",
    "Curso",
    "Disciplina",
    "CursoDisciplina",
    "DisciplinaPreRequisito",
    "MetricaDesempenho",
    "EstatisticaCurso",
    "User",
    "Recurso",
    "Dica",
    "Dificuldade",
    "Comentario",
    "AvaliacaoDisciplina",
    "Upvote"
]
