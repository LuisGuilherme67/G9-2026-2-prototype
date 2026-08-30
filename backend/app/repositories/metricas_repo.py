from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.metrica import MetricaDesempenho, EstatisticaCurso
from app.models.disciplina import Disciplina

class MetricasRepository:
    def get_by_disciplina(
        self, db: Session, disciplina_id: int, curso_id: Optional[int] = None
    ) -> List[MetricaDesempenho]:
        query = db.query(MetricaDesempenho).filter(MetricaDesempenho.disciplina_id == disciplina_id)
        if curso_id:
            query = query.filter(MetricaDesempenho.curso_id == curso_id)
        return query.order_by(MetricaDesempenho.ano.desc(), MetricaDesempenho.periodo.desc()).all()

    def get_historico_agregado(self, db: Session, disciplina_id: int) -> Dict[str, Any]:
        """Calcula a média histórica agregada de aprovação e reprovação de uma cadeira."""
        res = db.query(
            func.sum(MetricaDesempenho.total_matriculados).label("total_matriculados"),
            func.sum(MetricaDesempenho.aprovados).label("total_aprovados"),
            func.sum(MetricaDesempenho.reprovados_nota).label("total_reprovados_nota"),
            func.sum(MetricaDesempenho.reprovados_falta).label("total_reprovados_falta"),
            func.sum(MetricaDesempenho.trancamentos).label("total_trancamentos"),
            func.avg(MetricaDesempenho.nota_media).label("media_geral_notas")
        ).filter(
            MetricaDesempenho.disciplina_id == disciplina_id,
            MetricaDesempenho.is_suppressed.is_(False)
        ).first()

        total = res.total_matriculados or 0
        aprovados = res.total_aprovados or 0
        reprovados = (res.total_reprovados_nota or 0) + (res.total_reprovados_falta or 0)
        trancamentos = res.total_trancamentos or 0

        taxa_aprovacao = round((aprovados / total * 100.0), 2) if total > 0 else 0.0
        taxa_reprovacao = round((reprovados / total * 100.0), 2) if total > 0 else 0.0
        taxa_trancamento = round((trancamentos / total * 100.0), 2) if total > 0 else 0.0
        media_notas = round(float(res.media_geral_notas), 2) if res.media_geral_notas else None

        return {
            "disciplina_id": disciplina_id,
            "total_historico_matriculados": total,
            "taxa_aprovacao_historica": taxa_aprovacao,
            "taxa_reprovacao_historica": taxa_reprovacao,
            "taxa_trancamento_historica": taxa_trancamento,
            "media_notas_historica": media_notas
        }

    def get_estatisticas_curso(self, db: Session, curso_id: int) -> List[EstatisticaCurso]:
        return db.query(EstatisticaCurso).filter(
            EstatisticaCurso.curso_id == curso_id
        ).order_by(EstatisticaCurso.ano.desc()).all()

metricas_repo = MetricasRepository()
