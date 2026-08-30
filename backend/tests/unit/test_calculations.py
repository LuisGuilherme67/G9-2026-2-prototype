import pytest
from app.domain.calculations import (
    calcular_taxa_aprovacao,
    calcular_taxa_reprovacao,
    calcular_taxa_trancamento,
    calcular_taxa_evasao,
    calcular_taxa_retencao,
    calcular_resumo_desempenho
)

def test_calcular_taxa_aprovacao():
    assert calcular_taxa_aprovacao(40, 50) == 80.0
    assert calcular_taxa_aprovacao(0, 50) == 0.0
    assert calcular_taxa_aprovacao(10, 0) == 0.0

def test_calcular_taxa_reprovacao():
    assert calcular_taxa_reprovacao(15, 60) == 25.0
    assert calcular_taxa_reprovacao(0, 0) == 0.0

def test_calcular_taxa_trancamento():
    assert calcular_taxa_trancamento(5, 50) == 10.0

def test_calcular_taxa_evasao():
    assert calcular_taxa_evasao(20, 100) == 20.0
    assert calcular_taxa_evasao(0, 0) == 0.0

def test_calcular_resumo_desempenho():
    resumo = calcular_resumo_desempenho(
        total_matriculados=100,
        aprovados=70,
        reprovados_nota=15,
        reprovados_falta=5,
        trancamentos=10
    )
    assert resumo["taxa_aprovacao"] == 70.0
    assert resumo["taxa_reprovacao"] == 20.0
    assert resumo["taxa_trancamento"] == 10.0
