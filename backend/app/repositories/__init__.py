"""Camada de Acesso a Dados e Repositórios SQLAlchemy."""
from app.repositories.base import CRUDBase
from app.repositories.metricas_repo import MetricasRepository
from app.repositories.disciplina_repo import DisciplinaRepository

__all__ = ["CRUDBase", "MetricasRepository", "DisciplinaRepository"]
