import re
from typing import Tuple, List

TERMOS_PROIBIDOS_DEFAULT = [
    # Lista base de termos ofensivos / spam para moderação da comunidade
    "palavrao_exemplo",
    "spam_link",
    "comprar_trabalho",
    "fraude_academica"
]

def sanitizar_texto(texto: str) -> str:
    """Remove espaços excessivos e caracteres de controle indesejados."""
    if not texto:
        return ""
    return re.sub(r"\s+", " ", texto).strip()


def verificar_conteudo_apropriado(
    texto: str,
    termos_proibidos: List[str] = None
) -> Tuple[bool, List[str]]:
    """
    Verifica se o conteúdo de um comentário ou postagem viola diretrizes éticas e de conduta.
    Retorna (is_valido, lista_de_violacoes).
    """
    if not texto or len(texto.strip()) < 3:
        return False, ["O texto deve conter no mínimo 3 caracteres."]

    if len(texto) > 4000:
        return False, ["O texto excede o limite máximo permitido de 4000 caracteres."]

    termos = termos_proibidos if termos_proibidos is not None else TERMOS_PROIBIDOS_DEFAULT
    texto_lower = texto.lower()
    violacoes = []

    for termo in termos:
        if re.search(rf"\b{re.escape(termo)}\b", texto_lower):
            violacoes.append(f"Contém termo restrito: '{termo}'")

    return (len(violacoes) == 0, violacoes)
