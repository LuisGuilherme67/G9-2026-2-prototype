-- =====================================================================
-- PROJETO TAMBURETEI - SCRIPT SQL INICIAL (PostgreSQL 16)
-- Descrição: Criação de tabelas, relacionamentos, constraints e índices.
-- =====================================================================

-- Habilita extensão para geração de UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================================
-- 1. TABELA DE USUÁRIOS
-- =====================================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student' CHECK (role IN ('admin', 'moderator', 'student')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =====================================================================
-- 2. TABELAS DE ESTRUTURA ACADÊMICA (CURSOS E CADEIRAS)
-- =====================================================================
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(20) UNIQUE,
    slug VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(30),
    slug VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    workload_hours INT CHECK (workload_hours > 0),
    credits INT CHECK (credits > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Relação N:N entre Curso e Cadeira (disciplinas por curso)
CREATE TABLE IF NOT EXISTS course_subjects (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    period INT CHECK (period > 0), -- Ex: 1 para 1º período (NULL para optativas sem período fixo)
    is_mandatory BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_course_subject UNIQUE (course_id, subject_id)
);

-- Pré-requisitos entre cadeiras
CREATE TABLE IF NOT EXISTS subject_prerequisites (
    id SERIAL PRIMARY KEY,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    prerequisite_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_subject_prerequisite UNIQUE (subject_id, prerequisite_id),
    CONSTRAINT chk_no_self_prerequisite CHECK (subject_id <> prerequisite_id)
);

-- =====================================================================
-- 3. CONTEÚDOS DAS CADEIRAS (MATERIAIS, DICAS E DIFICULDADES)
-- =====================================================================

-- Materiais de estudo: Resumos, Provas Antigas, Links Úteis, Slides, Extras
CREATE TABLE IF NOT EXISTS resources (
    id BIGSERIAL PRIMARY KEY,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(30) NOT NULL CHECK (category IN ('resumo', 'prova', 'link_util', 'extra', 'slide')),
    url TEXT NOT NULL,
    semester VARCHAR(10), -- Ex: '2023.2'
    is_approved BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Dicas de estudo e conselhos
CREATE TABLE IF NOT EXISTS tips (
    id BIGSERIAL PRIMARY KEY,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Dificuldades comuns (pontos críticos onde os alunos mais trancam/reprovam)
CREATE TABLE IF NOT EXISTS difficulties (
    id BIGSERIAL PRIMARY KEY,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    topic VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =====================================================================
-- 4. COMUNIDADE, COMENTÁRIOS E AVALIAÇÕES
-- =====================================================================

-- Comentários (podem ser feitos em Dicas, Dificuldades ou Materiais)
CREATE TABLE IF NOT EXISTS comments (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL CHECK (target_type IN ('difficulty', 'tip', 'resource')),
    target_id BIGINT NOT NULL,
    parent_id BIGINT REFERENCES comments(id) ON DELETE CASCADE, -- Respostas aninhadas / threads
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Avaliações gerais e estatísticas da cadeira
CREATE TABLE IF NOT EXISTS subject_reviews (
    id BIGSERIAL PRIMARY KEY,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    difficulty_score INT NOT NULL CHECK (difficulty_score BETWEEN 1 AND 5),
    workload_score INT NOT NULL CHECK (workload_score BETWEEN 1 AND 5),
    status VARCHAR(20) NOT NULL CHECK (status IN ('aprovado', 'reprovado', 'trancou', 'cursando')),
    general_feedback TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_subject_review UNIQUE (subject_id, user_id)
);

-- Votos / Upvotes (curtidas em conteúdos e comentários)
CREATE TABLE IF NOT EXISTS upvotes (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL CHECK (target_type IN ('tip', 'resource', 'difficulty', 'comment')),
    target_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_target_upvote UNIQUE (user_id, target_type, target_id)
);

-- =====================================================================
-- 5. ÍNDICES PARA PERFORMANCE
-- =====================================================================
CREATE INDEX IF NOT EXISTS idx_courses_slug ON courses(slug);
CREATE INDEX IF NOT EXISTS idx_subjects_slug ON subjects(slug);
CREATE INDEX IF NOT EXISTS idx_course_subjects_course ON course_subjects(course_id);
CREATE INDEX IF NOT EXISTS idx_course_subjects_subject ON course_subjects(subject_id);

CREATE INDEX IF NOT EXISTS idx_resources_subject_category ON resources(subject_id, category);
CREATE INDEX IF NOT EXISTS idx_tips_subject ON tips(subject_id);
CREATE INDEX IF NOT EXISTS idx_difficulties_subject ON difficulties(subject_id);

CREATE INDEX IF NOT EXISTS idx_comments_target ON comments(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_comments_parent ON comments(parent_id);

CREATE INDEX IF NOT EXISTS idx_subject_reviews_subject ON subject_reviews(subject_id);
CREATE INDEX IF NOT EXISTS idx_upvotes_target ON upvotes(target_type, target_id);

-- =====================================================================
-- 6. DADOS INICIAIS DE TESTE (SEED DATA)
-- =====================================================================
INSERT INTO courses (name, code, slug) VALUES 
('Ciência da Computação', 'CC-UFCG', 'ciencia-da-computacao')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO subjects (name, code, slug, description, workload_hours, credits) VALUES 
('Programação I', '1411167', 'programacao-1', 'Introdução ao desenvolvimento de software, lógica e estruturas básicas.', 60, 4),
('Laboratório de Programação I', '1411168', 'lab-programacao-1', 'Prática laboratorial com resolução de problemas e testes.', 60, 4),
('Cálculo Diferencial e Integral I', '1109103', 'calculo-1', 'Limites, derivadas, integrais de funções de uma variável real.', 60, 4),
('Estruturas de Dados', '1411180', 'estruturas-de-dados', 'Listas, pilhas, filas, árvores, grafos e análise assintótica.', 60, 4)
ON CONFLICT (slug) DO NOTHING;

-- Vinculando matérias ao curso de Computação (1º e 2º períodos)
INSERT INTO course_subjects (course_id, subject_id, period, is_mandatory)
SELECT c.id, s.id, 1, TRUE FROM courses c, subjects s WHERE c.slug = 'ciencia-da-computacao' AND s.slug IN ('programacao-1', 'lab-programacao-1', 'calculo-1')
ON CONFLICT DO NOTHING;

INSERT INTO course_subjects (course_id, subject_id, period, is_mandatory)
SELECT c.id, s.id, 2, TRUE FROM courses c, subjects s WHERE c.slug = 'ciencia-da-computacao' AND s.slug = 'estruturas-de-dados'
ON CONFLICT DO NOTHING;

-- Definindo que Programação I é pré-requisito de Estruturas de Dados
INSERT INTO subject_prerequisites (subject_id, prerequisite_id)
SELECT s1.id, s2.id 
FROM subjects s1, subjects s2 
WHERE s1.slug = 'estruturas-de-dados' AND s2.slug = 'programacao-1'
ON CONFLICT DO NOTHING;
