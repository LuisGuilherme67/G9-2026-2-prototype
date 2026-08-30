# 📊 Tamburetei UnB — Métodos de Desenvolvimento de Software (MDS 2026/2)

Plataforma de Dados Acadêmicos Abertos e Hub Colaborativo de Apoio ao Estudante da **Universidade de Brasília (UnB)**, desenvolvido pelo **Grupo G9**.

---

## 🏛️ Arquitetura do Backend

O backend foi construído seguindo princípios de **Clean Architecture** / **Arquitetura em Camadas**, garantindo isolamento de regras de negócio, facilidade de testes em milissegundos e conformidade estrita com a **LGPD (K-Anonimato)**.

```
backend/
├── app/
│   ├── api/                 # Camada de Apresentação (FastAPI)
│   │   ├── v1/
│   │   │   ├── routers/     # Endpoints HTTP (analytics.py, cadeiras.py, auth.py)
│   │   │   └── schemas/     # Contratos Pydantic (Validação de entrada/saída)
│   │   └── deps.py          # Injeção de dependências (Session do DB, Auth)
│   │
│   ├── core/                # Configurações Globais (.env, JWT, DB Engine)
│   ├── domain/              # Camada de Negócio / Regras Puras (Isolada de I/O)
│   │   ├── calculations.py  # Fórmulas de evasão, retenção e aprovação
│   │   ├── anonymizer.py    # Algoritmo de supressão por K-Anonimato (< 5)
│   │   └── moderation.py    # Filtro de termos e regras de conduta
│   │
│   ├── services/            # Camada de Aplicação / Casos de Uso
│   │   ├── analytics_svc.py # Orquestração das consultas analíticas
│   │   └── cadeira_svc.py   # Orquestração do hub de matérias e comentários
│   │
│   ├── repositories/        # Camada de Acesso a Dados (SQLAlchemy)
│   │   ├── base.py          # Repositório genérico com operações CRUD
│   │   └── metricas_repo.py # Queries otimizadas e agregações no Postgres
│   │
│   └── models/              # Modelos Relacionais (SQLAlchemy ORM)
│       ├── curso.py
│       ├── disciplina.py
│       ├── metrica.py
│       └── conteudo.py
│
├── pipeline/                # Módulo de Ingestão de Dados (Foco R1)
│   ├── extractors/          # Parsers de CSV, XLSX e tabelas DPO/INEP
│   ├── transformers/        # Normalização e mascaramento de identificadores
│   └── loaders/             # Carga em lote no banco
│
├── alembic/                 # Migrações versionadas do banco de dados
└── tests/                   # Suíte de Testes (Unitários, Integração e Mutação)
    ├── unit/                # Testes em domain/ (Roda em milissegundos sem DB)
    ├── integration/         # Testes de endpoints com TestClient e DB de teste
    └── mutation/            # Configurações do Mutmut / Cosmic Ray
```

---

## 🚀 Como Executar o Projeto com Docker

### 1. Clonar e configurar ambiente
```bash
cp .env.example .env
```

### 2. Subir os serviços com Docker Compose
```bash
docker compose up -d --build
```

Serviços disponíveis:
- **API FastAPI (Docs Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Painel Adminer (Banco de Dados)**: [http://localhost:8080](http://localhost:8080)
- **PostgreSQL**: `localhost:5432`

---

## 🗄️ Migrações de Banco de Dados com Alembic

O versionamento do banco de dados é automatizado com **Alembic**.

### Aplicar todas as migrações:
```bash
docker compose exec backend alembic upgrade head
```

### Criar uma nova migração após alterar os modelos:
```bash
docker compose exec backend alembic revision --autogenerate -m "descricao_da_mudanca"
```

---

## 🧪 Como Rodar os Testes

### Rodar todos os testes (Unitários + Integração):
```bash
docker compose exec backend pytest -v
```

### Rodar apenas testes unitários rápidos de domínio:
```bash
docker compose exec backend pytest tests/unit -v
```

---

## 📦 Pipeline de Dados (Release 1)

Para executar o pipeline de extração, limpeza, anonimização LGPD e carga:
```bash
docker compose exec backend python pipeline/run_pipeline.py
```
