import pytest
from app.domain.moderation import sanitizar_texto, verificar_conteudo_apropriado

def test_sanitizar_texto():
    assert sanitizar_texto("  texto   com    espaços  ") == "texto com espaços"
    assert sanitizar_texto("") == ""

def test_verificar_conteudo_valido():
    valido, erros = verificar_conteudo_apropriado("Essa matéria tem uma ementa bem completa sobre árvores AVL e grafos.")
    assert valido is True
    assert len(erros) == 0

def test_verificar_conteudo_invalido_tamanho():
    valido, erros = verificar_conteudo_apropriado("a")
    assert valido is False
    assert len(erros) > 0

def test_verificar_conteudo_proibido():
    valido, erros = verificar_conteudo_apropriado("acesse aqui o link para comprar_trabalho urgente")
    assert valido is False
    assert any("comprar_trabalho" in e for e in erros)
