# 💻 Guia de Desenvolvimento

## 🚀 Como Subir o Projeto com Docker

### 1. Configurar variáveis de ambiente
Copie o modelo de variáveis de ambiente na raiz do projeto:
```bash
cp .env.example .env
```

### 2. Construir e iniciar os contêineres
```bash
docker compose up -d --build
```

Serviços disponibilizados:
* **API FastAPI (Swagger Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **OpenAPI JSON:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
* **Adminer (Interface do Banco de Dados):** [http://localhost:8080](http://localhost:8080)
* **PostgreSQL:** `localhost:5432`

---

## 🗄️ Migrações de Banco com Alembic

O controle do banco de dados é automatizado:

### Aplicar todas as migrações:
```bash
docker compose exec backend alembic upgrade head
```

### Gerar uma nova revisão automática após alterar modelos:
```bash
docker compose exec backend alembic revision --autogenerate -m "descricao_da_alteracao"
```

---

## 🧪 Testes Automatizados

### Executar a suíte completa de testes:
```bash
docker compose exec backend pytest -v
```

### Executar testes rápidos de domínio com relatório de cobertura:
```bash
docker compose exec backend pytest tests/unit -v --cov=app/domain --cov-report=term-missing
```

---

## 📖 Visualizar e Construir a Documentação (MkDocs)

Para visualizar esta documentação localmente em tempo real com recarregamento automático:

```bash
mkdocs serve
```
Acesse no seu navegador: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Para gerar os arquivos estáticos de documentação para publicação (HTML em `site/`):
```bash
mkdocs build
```
