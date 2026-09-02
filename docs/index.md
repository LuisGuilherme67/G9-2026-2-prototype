# 📊 Tamburetei UnB

Bem-vindo à documentação oficial do **Tamburetei UnB**, uma plataforma aberta, colaborativa e analítica voltada à comunidade acadêmica da **Universidade de Brasília (UnB)**, hospedada sob a organização **OpenDevUnB**.

O projeto é desenvolvido no âmbito da disciplina **Métodos de Desenvolvimento de Software (MDS 2026/2 — FCTE/UnB)** pelo **Grupo G9**, inspirado pelo ecossistema do OpenDevUFCG.

---

## 🎯 Propósito do Sistema

O sistema foi concebido para resolver duas demandas centrais dos estudantes e pesquisadores da UnB:

### 1. Transparência e Métricas Acadêmicas
Ingestão, anonimização e disponibilização de dados analíticos oficiais obtidos via DPO, INEP e Lei de Acesso à Informação (LAI):
* **Taxas de aprovação** por disciplina, semestre e departamento;
* **Reprovação** por nota e por frequência/falta;
* **Trancamentos e retenção** acadêmica;
* **Taxas de evasão** por curso;
* **Tempo médio de formação**.

### 2. Hub Colaborativo de Disciplinas (`/cadeiras`)
Centralização de conteúdos e materiais de apoio acadêmico gerados pela comunidade:
* Ementas e fluxogramas recomendados;
* Dificuldades comuns e relatos moderados;
* Dicas de estudo e resumos de conteúdos (*"leites"*);
* Links úteis e provas/avaliações públicas anteriores.

---

## 🗓️ Cronograma e Entregas (Releases)

| Release | Data Limite | Foco Principal | Entregáveis Técnicos |
| :--- | :--- | :--- | :--- |
| **Release 1 (R1)** | Semana 7 — 28/09/2026 | Engenharia de Dados & Infraestrutura | Pipeline ETL conteinerizado em Docker, anonimização LGPD ($k$-anonimato), dataset limpo e modelos relacionais no PostgreSQL com Alembic. |
| **Release 2 (R2)** | Semana 15 — 25/11/2026 | Portal Web & Hub Comunitário | Frontend em Next.js com App Router, dashboards analíticos, hub de disciplinas (`/cadeiras/:slug`), moderação e pipeline CI/CD com SAST. |

---

## 🛠️ Stack Tecnológica

* **Backend:** Python 3.12+, FastAPI (arquitetura assíncrona), Pydantic v2 e SQLAlchemy 2.0.
* **Banco de Dados:** PostgreSQL 17 gerenciado via Docker e migrações versionadas com Alembic.
* **Frontend (R2):** Next.js (App Router), React, TypeScript e Tailwind CSS.
* **Qualidade & Testes:** Pytest, Mutmut (testes de mutação), Bandit e SonarQube (SAST).
* **Infraestrutura:** Docker e Docker Compose para execução isolada e reprodutível.
