from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime, String, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class MetricaDesempenho(Base):
    __tablename__ = "metricas_desempenho"

    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=True, index=True)
    ano = Column(Integer, nullable=False, index=True)
    periodo = Column(Integer, nullable=False, index=True) # 1 ou 2 (Ex: 2023.1)
    
    total_matriculados = Column(Integer, nullable=False, default=0)
    aprovados = Column(Integer, nullable=False, default=0)
    reprovados_nota = Column(Integer, nullable=False, default=0)
    reprovados_falta = Column(Integer, nullable=False, default=0)
    trancamentos = Column(Integer, nullable=False, default=0)
    
    taxa_aprovacao = Column(Float, nullable=True) # %
    taxa_reprovacao = Column(Float, nullable=True) # %
    taxa_trancamento = Column(Float, nullable=True) # %
    nota_media = Column(Float, nullable=True)
    
    # Flag LGPD: se total_matriculados < k_threshold (ex: 5), dados detalhados são suprimidos
    is_suppressed = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    disciplina = relationship("Disciplina", back_populates="metricas")
    curso = relationship("Curso", back_populates="metricas")

    __table_args__ = (
        UniqueConstraint("disciplina_id", "curso_id", "ano", "periodo", name="uq_metrica_disciplina_periodo"),
    )

    def __repr__(self):
        return f"<MetricaDesempenho(disciplina_id={self.disciplina_id}, ano={self.ano}.{self.periodo}, aprovacao={self.taxa_aprovacao}%)>"


class EstatisticaCurso(Base):
    __tablename__ = "estatisticas_curso"

    id = Column(Integer, primary_key=True, index=True)
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False, index=True)
    ano = Column(Integer, nullable=False, index=True)
    
    taxa_evasao = Column(Float, nullable=True) # %
    taxa_retencao = Column(Float, nullable=True) # %
    tempo_medio_formacao = Column(Float, nullable=True) # em semestres
    total_alunos_ativos = Column(Integer, nullable=True)
    total_formados = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
