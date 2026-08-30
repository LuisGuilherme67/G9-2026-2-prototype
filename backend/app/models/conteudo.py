import uuid
from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, ForeignKey, DateTime, func, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="student", nullable=False) # 'admin', 'moderator', 'student'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos
    recursos = relationship("Recurso", back_populates="autor")
    dicas = relationship("Dica", back_populates="autor")
    dificuldades = relationship("Dificuldade", back_populates="autor")
    comentarios = relationship("Comentario", back_populates="autor")
    avaliacoes = relationship("AvaliacaoDisciplina", back_populates="autor")
    upvotes = relationship("Upvote", back_populates="user")


class Recurso(Base):
    __tablename__ = "recursos"

    id = Column(BigInteger, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(30), nullable=False) # 'resumo', 'prova', 'link_util', 'extra', 'slide'
    url = Column(Text, nullable=False)
    semester = Column(String(10), nullable=True) # Ex: '2023.2'
    is_approved = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    disciplina = relationship("Disciplina", back_populates="recursos")
    autor = relationship("User", back_populates="recursos")


class Dica(Base):
    __tablename__ = "dicas"

    id = Column(BigInteger, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    disciplina = relationship("Disciplina", back_populates="dicas")
    autor = relationship("User", back_populates="dicas")


class Dificuldade(Base):
    __tablename__ = "dificuldades"

    id = Column(BigInteger, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    topic = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    disciplina = relationship("Disciplina", back_populates="dificuldades")
    autor = relationship("User", back_populates="dificuldades")


class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_type = Column(String(20), nullable=False, index=True) # 'difficulty', 'tip', 'resource'
    target_id = Column(BigInteger, nullable=False, index=True)
    parent_id = Column(BigInteger, ForeignKey("comentarios.id", ondelete="CASCADE"), nullable=True, index=True)
    content = Column(Text, nullable=False)
    is_moderated = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    autor = relationship("User", back_populates="comentarios")
    respostas = relationship("Comentario", backref="parent", remote_side=[id], cascade="all, delete-orphan")


class AvaliacaoDisciplina(Base):
    __tablename__ = "avaliacoes_disciplina"

    id = Column(BigInteger, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    difficulty_score = Column(Integer, nullable=False) # 1 a 5
    workload_score = Column(Integer, nullable=False) # 1 a 5
    status = Column(String(20), nullable=False) # 'aprovado', 'reprovado', 'trancou', 'cursando'
    general_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    disciplina = relationship("Disciplina", back_populates="avaliacoes")
    autor = relationship("User", back_populates="avaliacoes")

    __table_args__ = (
        UniqueConstraint("disciplina_id", "user_id", name="uq_user_subject_review"),
        CheckConstraint("difficulty_score >= 1 AND difficulty_score <= 5", name="chk_difficulty_score_range"),
        CheckConstraint("workload_score >= 1 AND workload_score <= 5", name="chk_workload_score_range"),
    )


class Upvote(Base):
    __tablename__ = "upvotes"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_type = Column(String(20), nullable=False, index=True) # 'tip', 'resource', 'difficulty', 'comment'
    target_id = Column(BigInteger, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="upvotes")

    __table_args__ = (
        UniqueConstraint("user_id", "target_type", "target_id", name="uq_user_target_upvote"),
    )
