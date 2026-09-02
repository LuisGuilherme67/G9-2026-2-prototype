# 📊 Tamburetei UnB

> Plataforma aberta, colaborativa e analítica voltada à comunidade acadêmica da **Universidade de Brasília (UnB)**, hospedada sob a organização **OpenDevUnB**.

Projeto desenvolvido no âmbito da disciplina **Métodos de Desenvolvimento de Software (MDS 2026/2 — FCTE/UnB)** pelo **Grupo G9**, inspirado no ecossistema do OpenDevUFCG.

---

## 🎯 Propósitos do Projeto

1. **Transparência e Métricas Acadêmicas:**
   - Ingestão e agregação de dados oficiais do DPO, INEP e LAI (taxas de aprovação, reprovação por nota e falta, trancamentos e evasão).
   - Anonimização estrita em conformidade com a LGPD através de $k$-anonimato ($< 5$ estudantes).
2. **Hub Colaborativo de Disciplinas (`/cadeiras`):**
   - Centralização de materiais de apoio (ementas, dificuldades comuns, resumos de conteúdos, links úteis e provas públicas antigas).
   - Moderação e proteção à integridade docente e acadêmica.

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.0 |
| **Banco de Dados** | PostgreSQL 17 gerenciado via Docker, Alembic para migrações |
| **Frontend (R2)** | Next.js (App Router), React, TypeScript, Tailwind CSS |
| **Documentação** | MkDocs |
| **Testes & Qualidade** | Pytest, Mutmut (mutação), Bandit e SonarQube (SAST) |
| **Infraestrutura** | Docker e Docker Compose |

---

## 🏛️ Arquitetura do Backend

O backend adota princípios de **Clean Architecture** e arquitetura em camadas para isolar a lógica de negócios da infraestrutura e viabilizar testes unitários em milissegundos sem conexão de banco:

```
backend/
├── app/
│   ├── api/                 # Camada HTTP (FastAPI): Routers e Schemas Pydantic
│   ├── core/                # Configurações globais (.env, banco, segurança)
│   ├── domain/              # Regras puras de negócio (cálculos de evasão, k-anonimato, moderação)
│   ├── services/            # Orquestração e casos de uso da aplicação
│   ├── repositories/        # Acesso a dados com SQLAlchemy ORM
│   └── models/              # Entidades relacionais do banco
├── pipeline/                # ETL: extração DPO/INEP, limpeza e anonimização
├── alembic/                 # Migrações versionadas do banco de dados
└── tests/                   # Suíte de testes automatizados (unitários, integração e mutação)
```

---

## 🚀 Como Executar o Projeto com Docker

### 1. Configurar variáveis de ambiente
```bash
cp .env.example .env
```

### 2. Iniciar os serviços
```bash
docker compose up -d --build
```

Serviços acessíveis:
* **API FastAPI (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Adminer (Painel DB):** [http://localhost:8080](http://localhost:8080)
* **PostgreSQL:** `localhost:5432`

---

## 🗄️ Migrações de Banco de Dados com Alembic

```bash
# Aplicar migrações pendentes
docker compose exec backend alembic upgrade head

# Gerar nova migração após alterar modelos
docker compose exec backend alembic revision --autogenerate -m "descricao_da_mudanca"
```

---

## 🧪 Como Rodar os Testes

```bash
# Executar todos os testes
docker compose exec backend pytest -v

# Executar testes unitários do domínio com cobertura
docker compose exec backend pytest tests/unit -v --cov=app/domain
```

---

## 📚 Documentação com MkDocs

A documentação detalhada do projeto está disponível na pasta `docs/`.

### Visualizar localmente:
```bash
mkdocs serve
```
Acesse: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Gerar build estático da documentação:
```bash
mkdocs build
```

---

## 👥 Equipe

Desenvolvido pelo **Grupo G9** — Disciplina de Métodos de Desenvolvimento de Software (MDS 2026/2), Faculdade de Ciências e Tecnologias em Engenharia (FCTE), Universidade de Brasília (UnB).
