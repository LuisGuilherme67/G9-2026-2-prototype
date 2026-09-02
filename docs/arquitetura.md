# 🏛️ Arquitetura e Decisões Técnicas

## Arquitetura em Camadas do Backend

O backend foi estruturado seguindo os princípios de isolamento de responsabilidades e **Clean Architecture**, permitindo testabilidade unitária ágil em milissegundos sem dependência de banco de dados ativo:

```
backend/app/
├── api/             # Routers HTTP do FastAPI e Schemas Pydantic (entrada/saída)
├── core/            # Configurações globais (.env, JWT, Engine do DB)
├── domain/          # Regras de negócio puras (cálculos de evasão, k-anonimato, moderação)
├── services/        # Casos de uso e orquestração entre API e repositórios
├── repositories/    # Consultas SQL e persistência via SQLAlchemy ORM
├── models/          # Entidades relacionais mapeadas com SQLAlchemy
└── pipeline/        # ETL: extração DPO/INEP, normalização e carga
```

---

## Modelo de Dados (PostgreSQL)

O esquema relacional é composto pelas seguintes tabelas principais:

* **`cursos`**: Metadados dos cursos de graduação (`codigo_mec`, `nome`, `campus`, `grau`, `turno`).
* **`disciplinas`**: Cadastro das matérias (`codigo`, `slug`, `nome`, `departamento`, `creditos`, `ementa`).
* **`cursos_disciplinas`**: Matriz curricular associando matérias aos semestres recomendados.
* **`metricas_academicas`**: Fato analítico agregado com dados de matrículas, aprovações, reprovações, trancamentos e flag `is_k_anonimizado`.
* **`conteudos`**: Recursos colaborativos (`LINK_UTIL`, `RESUMO`, `PROVA_ANTIGA`, `DICA`) com controle de curadoria.
* **`comentarios`**: Relatos acadêmicos sobre disciplinas, com moderação de conteúdo e garantia de conduta.

---

## Decisões Arquiteturais (ADRs)

### ADR 01: Rejeição de Redis e Bancos NoSQL
* **Decisão:** Não utilizar Redis nem bancos NoSQL (como MongoDB) para cache ou armazenamento no escopo atual.
* **Justificativa:** Evitar sobre-engenharia (*over-engineering*) e custos de manutenção no CI/CD. O PostgreSQL com índices adequados atende tranquilamente às consultas analíticas em menos de 300 ms.

### ADR 02: Database-as-Code com Alembic
* **Decisão:** Todas as modificações no banco de dados devem ser registradas via migrações versionadas do Alembic.
* **Justificativa:** É estritamente vedada a execução de comandos DDL manuais no ambiente de produção ou desenvolvimento, garantindo rastreabilidade e reprodutibilidade.
