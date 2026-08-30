from typing import Dict, Optional

def calcular_taxa_aprovacao(aprovados: int, total_matriculados: int) -> float:
    """Calcula a taxa percentual de aprovação."""
    if total_matriculados <= 0:
        return 0.0
    return round((aprovados / total_matriculados) * 100.0, 2)


def calcular_taxa_reprovacao(reprovados_total: int, total_matriculados: int) -> float:
    """Calcula a taxa percentual de reprovação (nota + falta)."""
    if total_matriculados <= 0:
        return 0.0
    return round((reprovados_total / total_matriculados) * 100.0, 2)


def calcular_taxa_trancamento(trancamentos: int, total_matriculados: int) -> float:
    """Calcula a taxa percentual de trancamento."""
    if total_matriculados <= 0:
        return 0.0
    return round((trancamentos / total_matriculados) * 100.0, 2)


def calcular_taxa_evasao(evadidos: int, ingressantes: int) -> float:
    """Calcula a taxa percentual de evasão de uma coorte/curso."""
    if ingressantes <= 0:
        return 0.0
    return round((evadidos / ingressantes) * 100.0, 2)


def calcular_taxa_retencao(alunos_retidos: int, total_esperado: int) -> float:
    """Calcula a taxa de retenção curricular."""
    if total_esperado <= 0:
        return 0.0
    return round((alunos_retidos / total_esperado) * 100.0, 2)


def calcular_resumo_desempenho(
    total_matriculados: int,
    aprovados: int,
    reprovados_nota: int,
    reprovados_falta: int,
    trancamentos: int
) -> Dict[str, float]:
    """Retorna o sumário completo de métricas percentuais de uma turma/disciplina."""
    reprovados_total = reprovados_nota + reprovados_falta
    return {
        "taxa_aprovacao": calcular_taxa_aprovacao(aprovados, total_matriculados),
        "taxa_reprovacao": calcular_taxa_reprovacao(reprovados_total, total_matriculados),
        "taxa_trancamento": calcular_taxa_trancamento(trancamentos, total_matriculados),
    }
