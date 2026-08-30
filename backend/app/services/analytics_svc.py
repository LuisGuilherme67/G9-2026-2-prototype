from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories.metricas_repo import metricas_repo
from app.repositories.disciplina_repo import disciplina_repo
from app.domain.calculations import calcular_resumo_desempenho
from app.domain.anonymizer import aplicar_k_anonimato
from app.core.config import settings

class AnalyticsService:
    def get_subject_metrics(
        self, db: Session, subject_slug: str, course_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Obtém métricas históricas de uma matéria com K-Anonimato e consolidação."""
        subject = disciplina_repo.get_by_slug(db, subject_slug)
        if not subject:
            return {}

        metricas_raw = metricas_repo.get_by_disciplina(db, subject.id, course_id)
        metricas_processadas = []

        for m in metricas_raw:
            dado_dict = {
                "id": m.id,
                "ano": m.ano,
                "periodo": m.periodo,
                "total_matriculados": m.total_matriculados,
                "aprovados": m.aprovados,
                "reprovados_nota": m.reprovados_nota,
                "reprovados_falta": m.reprovados_falta,
                "trancamentos": m.trancamentos,
                "taxa_aprovacao": m.taxa_aprovacao,
                "taxa_reprovacao": m.taxa_reprovacao,
                "taxa_trancamento": m.taxa_trancamento,
                "nota_media": m.nota_media
            }
            # Aplica regra de supressão LGPD
            dado_protegido = aplicar_k_anonimato(
                dado_dict,
                k_threshold=settings.K_ANONYMITY_THRESHOLD,
                campo_contagem="total_matriculados"
            )
            metricas_processadas.append(dado_protegido)

        historico_agregado = metricas_repo.get_historico_agregado(db, subject.id)

        return {
            "disciplina": {
                "id": subject.id,
                "nome": subject.name,
                "codigo": subject.code,
                "slug": subject.slug
            },
            "resumo_historico": historico_agregado,
            "series_temporais": metricas_processadas
        }

    def get_course_analytics(self, db: Session, course_id: int) -> List[Dict[str, Any]]:
        stats = metricas_repo.get_estatisticas_curso(db, course_id)
        return [
            {
                "ano": s.ano,
                "taxa_evasao": s.taxa_evasao,
                "taxa_retencao": s.taxa_retencao,
                "tempo_medio_formacao": s.tempo_medio_formacao,
                "total_alunos_ativos": s.total_alunos_ativos,
                "total_formados": s.total_formados
            }
            for s in stats
        ]

analytics_service = AnalyticsService()
