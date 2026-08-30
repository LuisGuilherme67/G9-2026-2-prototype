import pytest
from app.domain.anonymizer import hash_identifier, aplicar_k_anonimato

def test_hash_identifier():
    h1 = hash_identifier("190012345")
    h2 = hash_identifier("190012345")
    h3 = hash_identifier("190054321")
    
    assert len(h1) == 64
    assert h1 == h2 # Determinístico com o mesmo salt
    assert h1 != h3

def test_aplicar_k_anonimato_amostra_pequena():
    # Amostra com menos de 5 alunos deve ser suprimida (LGPD)
    registro = {
        "disciplina_id": 1,
        "total_matriculados": 3,
        "aprovados": 3,
        "reprovados_nota": 0,
        "nota_media": 9.5
    }
    resultado = aplicar_k_anonimato(registro, k_threshold=5)
    assert resultado["is_suppressed"] is True
    assert resultado["aprovados"] is None
    assert resultado["nota_media"] is None
    assert "LGPD" in resultado["aviso_lgpd"]

def test_aplicar_k_anonimato_amostra_suficiente():
    # Amostra >= 5 não deve sofrer supressão
    registro = {
        "disciplina_id": 1,
        "total_matriculados": 45,
        "aprovados": 35,
        "reprovados_nota": 10,
        "nota_media": 7.2
    }
    resultado = aplicar_k_anonimato(registro, k_threshold=5)
    assert resultado["is_suppressed"] is False
    assert resultado["aprovados"] == 35
    assert resultado["nota_media"] == 7.2
    assert resultado["aviso_lgpd"] is None
