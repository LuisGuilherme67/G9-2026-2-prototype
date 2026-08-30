from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class MetricaSerieTemporal(BaseModel):
    id: int
    ano: int
    periodo: int
    total_matriculados: int
    aprovados: Optional[int] = None
    reprovados_nota: Optional[int] = None
    reprovados_falta: Optional[int] = None
    trancamentos: Optional[int] = None
    taxa_aprovacao: Optional[float] = None
    taxa_reprovacao: Optional[float] = None
    taxa_trancamento: Optional[float] = None
    nota_media: Optional[float] = None
    is_suppressed: bool = False
    aviso_lgpd: Optional[str] = None

class ResumoHistorico(BaseModel):
    disciplina_id: int
    total_historico_matriculados: int
    taxa_aprovacao_historica: float
    taxa_reprovacao_historica: float
    taxa_trancamento_historica: float
    media_notas_historica: Optional[float] = None

class DisciplinaShort(BaseModel):
    id: int
    nome: str
    codigo: Optional[str] = None
    slug: str

class SubjectAnalyticsResponse(BaseModel):
    disciplina: DisciplinaShort
    resumo_historico: ResumoHistorico
    series_temporais: List[MetricaSerieTemporal]

class CursoAnalyticsResponse(BaseModel):
    ano: int
    taxa_evasao: Optional[float] = None
    taxa_retencao: Optional[float] = None
    tempo_medio_formacao: Optional[float] = None
    total_alunos_ativos: Optional[int] = None
    total_formados: Optional[int] = None
