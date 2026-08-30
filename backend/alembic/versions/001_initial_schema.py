"""initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-30 15:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criação da tabela de Usuários
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(150), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='student'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Criação da tabela de Cursos
    op.create_table(
        'cursos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('code', sa.String(20), nullable=True, unique=True),
        sa.Column('slug', sa.String(150), nullable=False, unique=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.create_index(op.f('ix_cursos_slug'), 'cursos', ['slug'], unique=True)
    op.create_index(op.f('ix_cursos_code'), 'cursos', ['code'], unique=True)

    # Criação da tabela de Disciplinas
    op.create_table(
        'disciplinas',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('code', sa.String(30), nullable=True),
        sa.Column('slug', sa.String(150), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('workload_hours', sa.Integer(), nullable=True),
        sa.Column('credits', sa.Integer(), nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.create_index(op.f('ix_disciplinas_slug'), 'disciplinas', ['slug'], unique=True)
    op.create_index(op.f('ix_disciplinas_code'), 'disciplinas', ['code'], unique=False)

    # Criação de Curso_Disciplinas (N:N)
    op.create_table(
        'curso_disciplinas',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subject_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('period', sa.Integer(), nullable=True),
        sa.Column('is_mandatory', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('course_id', 'subject_id', name='uq_course_subject')
    )

    # Criação de Disciplina_PreRequisitos
    op.create_table(
        'disciplina_prerequisitos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('disciplina_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('prerequisite_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('disciplina_id', 'prerequisite_id', name='uq_subject_prerequisite'),
        sa.CheckConstraint('disciplina_id != prerequisite_id', name='chk_no_self_prerequisite')
    )

    # Criação de Metricas de Desempenho
    op.create_table(
        'metricas_desempenho',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('disciplina_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('curso_id', sa.Integer(), sa.ForeignKey('cursos.id', ondelete='CASCADE'), nullable=True),
        sa.Column('ano', sa.Integer(), nullable=False),
        sa.Column('periodo', sa.Integer(), nullable=False),
        sa.Column('total_matriculados', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('aprovados', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reprovados_nota', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reprovados_falta', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('trancamentos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('taxa_aprovacao', sa.Float(), nullable=True),
        sa.Column('taxa_reprovacao', sa.Float(), nullable=True),
        sa.Column('taxa_trancamento', sa.Float(), nullable=True),
        sa.Column('nota_media', sa.Float(), nullable=True),
        sa.Column('is_suppressed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('disciplina_id', 'curso_id', 'ano', 'periodo', name='uq_metrica_disciplina_periodo')
    )
    op.create_index(op.f('ix_metricas_desempenho_ano'), 'metricas_desempenho', ['ano'], unique=False)
    op.create_index(op.f('ix_metricas_desempenho_periodo'), 'metricas_desempenho', ['periodo'], unique=False)

    # Criação de Estatisticas de Curso
    op.create_table(
        'estatisticas_curso',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('curso_id', sa.Integer(), sa.ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False),
        sa.Column('ano', sa.Integer(), nullable=False),
        sa.Column('taxa_evasao', sa.Float(), nullable=True),
        sa.Column('taxa_retencao', sa.Float(), nullable=True),
        sa.Column('tempo_medio_formacao', sa.Float(), nullable=True),
        sa.Column('total_alunos_ativos', sa.Integer(), nullable=True),
        sa.Column('total_formados', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    # Criação de Recursos (Provas, Resumos, etc.)
    op.create_table(
        'recursos',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('disciplina_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(30), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('semester', sa.String(10), nullable=True),
        sa.Column('is_approved', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    # Criação de Dicas
    op.create_table(
        'dicas',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('disciplina_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    # Criação de Dificuldades
    op.create_table(
        'dificuldades',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('disciplina_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('topic', sa.String(150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    # Criação de Comentarios
    op.create_table(
        'comentarios',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_type', sa.String(20), nullable=False),
        sa.Column('target_id', sa.BigInteger(), nullable=False),
        sa.Column('parent_id', sa.BigInteger(), sa.ForeignKey('comentarios.id', ondelete='CASCADE'), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_moderated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.create_index(op.f('ix_comentarios_target'), 'comentarios', ['target_type', 'target_id'], unique=False)

    # Criação de Avaliacoes
    op.create_table(
        'avaliacoes_disciplina',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('disciplina_id', sa.Integer(), sa.ForeignKey('disciplinas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('difficulty_score', sa.Integer(), nullable=False),
        sa.Column('workload_score', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('general_feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('disciplina_id', 'user_id', name='uq_user_subject_review'),
        sa.CheckConstraint('difficulty_score >= 1 AND difficulty_score <= 5', name='chk_difficulty_score_range'),
        sa.CheckConstraint('workload_score >= 1 AND workload_score <= 5', name='chk_workload_score_range')
    )

    # Criação de Upvotes
    op.create_table(
        'upvotes',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_type', sa.String(20), nullable=False),
        sa.Column('target_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('user_id', 'target_type', 'target_id', name='uq_user_target_upvote')
    )


def downgrade() -> None:
    op.drop_table('upvotes')
    op.drop_table('avaliacoes_disciplina')
    op.drop_table('comentarios')
    op.drop_table('dificuldades')
    op.drop_table('dicas')
    op.drop_table('recursos')
    op.drop_table('estatisticas_curso')
    op.drop_table('metricas_desempenho')
    op.drop_table('disciplina_prerequisitos')
    op.drop_table('curso_disciplinas')
    op.drop_table('disciplinas')
    op.drop_table('cursos')
    op.drop_table('users')
