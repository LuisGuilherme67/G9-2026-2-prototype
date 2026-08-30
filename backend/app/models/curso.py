from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, index=True, nullable=True)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    curso_disciplinas = relationship("CursoDisciplina", back_populates="curso", cascade="all, delete-orphan")
    metricas = relationship("MetricaDesempenho", back_populates="curso", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Curso(id={self.id}, name='{self.name}', slug='{self.slug}')>"
