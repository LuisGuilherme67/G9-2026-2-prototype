from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(30), index=True, nullable=True)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    workload_hours = Column(Integer, nullable=True)
    credits = Column(Integer, nullable=True)
    department = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    curso_disciplinas = relationship("CursoDisciplina", back_populates="disciplina", cascade="all, delete-orphan")
    
    # Pré-requisitos
    requisitos = relationship(
        "DisciplinaPreRequisito",
        foreign_keys="DisciplinaPreRequisito.disciplina_id",
        back_populates="disciplina",
        cascade="all, delete-orphan"
    )
    e_requisito_de = relationship(
        "DisciplinaPreRequisito",
        foreign_keys="DisciplinaPreRequisito.prerequisite_id",
        back_populates="prerequisite",
        cascade="all, delete-orphan"
    )

    # Conteúdos
    recursos = relationship("Recurso", back_populates="disciplina", cascade="all, delete-orphan")
    dicas = relationship("Dica", back_populates="disciplina", cascade="all, delete-orphan")
    dificuldades = relationship("Dificuldade", back_populates="disciplina", cascade="all, delete-orphan")
    avaliacoes = relationship("AvaliacaoDisciplina", back_populates="disciplina", cascade="all, delete-orphan")
    metricas = relationship("MetricaDesempenho", back_populates="disciplina", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Disciplina(id={self.id}, name='{self.name}', slug='{self.slug}')>"


class CursoDisciplina(Base):
    __tablename__ = "curso_disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    period = Column(Integer, nullable=True) # 1º período, 2º período, etc.
    is_mandatory = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    curso = relationship("Curso", back_populates="curso_disciplinas")
    disciplina = relationship("Disciplina", back_populates="curso_disciplinas")

    __table_args__ = (
        UniqueConstraint("course_id", "subject_id", name="uq_course_subject"),
    )


class DisciplinaPreRequisito(Base):
    __tablename__ = "disciplina_prerequisitos"

    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    prerequisite_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    disciplina = relationship("Disciplina", foreign_keys=[disciplina_id], back_populates="requisitos")
    prerequisite = relationship("Disciplina", foreign_keys=[prerequisite_id], back_populates="e_requisito_de")

    __table_args__ = (
        UniqueConstraint("disciplina_id", "prerequisite_id", name="uq_subject_prerequisite"),
        CheckConstraint("disciplina_id != prerequisite_id", name="chk_no_self_prerequisite")
    )
