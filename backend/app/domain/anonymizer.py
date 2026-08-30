import hashlib
from typing import Dict, Any, Optional

def hash_identifier(identifier: str, salt: str = "unb_tamburetei_mds_2026") -> str:
    """Gera um hash SHA-256 irreversível para pseudonimização de matrículas/identificadores."""
    if not identifier:
        return ""
    combined = f"{identifier}:{salt}".encode("utf-8")
    return hashlib.sha256(combined).hexdigest()


def aplicar_k_anonimato(
    registro: Dict[str, Any],
    k_threshold: int = 5,
    campo_contagem: str = "total_matriculados"
) -> Dict[str, Any]:
    """
    Aplica a regra de supressão de K-Anonimato (LGPD).
    Se o número de alunos em uma amostra for menor que `k_threshold` (ex: < 5),
    os valores absolutos sensíveis (notas detalhadas, contagens exatas) são suprimidos
    para evitar reidentificação indireta de estudantes.
    """
    resultado = dict(registro)
    contagem = resultado.get(campo_contagem, 0) or 0
    
    if contagem < k_threshold:
        resultado["is_suppressed"] = True
        resultado["aprovados"] = None
        resultado["reprovados_nota"] = None
        resultado["reprovados_falta"] = None
        resultado["trancamentos"] = None
        resultado["nota_media"] = None
        resultado["aviso_lgpd"] = f"Dados detalhados suprimidos por conformidade LGPD (amostra < {k_threshold} discentes)."
    else:
        resultado["is_suppressed"] = False
        resultado["aviso_lgpd"] = None

    return resultado
