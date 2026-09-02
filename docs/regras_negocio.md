# ⚖️ Regras de Negócio e Governança

O projeto obedece obrigatoriamente a diretrizes estritas de privacidade, conformidade legal e ética acadêmica:

---

## Regras de Negócio

### [RN01] K-Anonimato e Conformidade com a LGPD
* Agregações de turmas, cursos ou amostras com **menos de 5 estudantes** devem ser suprimidas ou agrupadas sob a notação especial `"< 5"`.
* É expressamente vedado armazenar ou expor dados pessoais identificáveis (DPI) como nome, CPF, e-mail institucional ou número de matrícula.

### [RN02] Proteção a Docentes e Ética
* É estritamente proibida a publicação de juízos depreciativos de valor ou ataques difamatórios a professores.
* Relatos e comentários devem focar exclusivamente na ementa, metodologia, bibliografia e dinâmicas pedagógicas da disciplina.

### [RN03] Vedação de Resoluções Ativas
* Não é permitida a disponibilização de respostas ou gabaritos de listas de exercícios, laboratórios ou atividades avaliativas recorrentes.
* São aceitos apenas enunciados de provas públicas antigas e materiais conceituais de estudo.

### [RN04] Fórmula para Cálculo de Evasão
* A taxa de evasão institucional deve ser computada seguindo a relação oficial:
  $$\text{Taxa de Evasão (\%)} = \left( \frac{\text{Total de Desligamentos}}{\text{Total de Matriculados Ativos}} \right) \times 100$$

---

## Critérios de Qualidade da Disciplina (MDS)

1. **Cobertura de Código:** Mínimo de **70% de cobertura** de linhas no módulo de domínio (`app/domain/`).
2. **Escore de Mutação:** Mínimo de **50% de mortes** de mutantes nas regras de negócio com Mutmut.
3. **Testes de Sabotagem:** A suíte de testes deve falhar com 100% de eficácia quando falhas forem intencionalmente injetadas no domínio.
4. **Análise Estática de Segurança (SAST):** Nenhuma vulnerabilidade crítica ou alta tolerada no pipeline.
5. **Reprodutibilidade:** Todo o ambiente deve subir integralmente via Docker Compose.
