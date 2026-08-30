import pandas as pd
from sqlalchemy.orm import Session
from app.models.curso import Curso
from app.models.disciplina import Disciplina
from app.models.metrica import MetricaDesempenho

class DatabaseLoader:
    def load_courses(self, db: Session, df: pd.DataFrame) -> int:
        count = 0
        for _, row in df.iterrows():
            slug = str(row.get("slug"))
            existing = db.query(Curso).filter(Curso.slug == slug).first()
            if not existing:
                curso = Curso(
                    name=row.get("name"),
                    code=row.get("code"),
                    slug=slug,
                    department=row.get("department")
                )
                db.add(curso)
                count += 1
        db.commit()
        return count

    def load_subjects(self, db: Session, df: pd.DataFrame) -> int:
        count = 0
        for _, row in df.iterrows():
            slug = str(row.get("slug"))
            existing = db.query(Disciplina).filter(Disciplina.slug == slug).first()
            if not existing:
                disciplina = Disciplina(
                    name=row.get("name"),
                    code=row.get("code"),
                    slug=slug,
                    description=row.get("description"),
                    workload_hours=row.get("workload_hours"),
                    credits=row.get("credits"),
                    department=row.get("department")
                )
                db.add(disciplina)
                count += 1
        db.commit()
        return count

    def load_metrics(self, db: Session, df: pd.DataFrame) -> int:
        count = 0
        for _, row in df.iterrows():
            disc_id = int(row.get("disciplina_id"))
            ano = int(row.get("ano"))
            periodo = int(row.get("periodo"))
            curso_id = int(row.get("curso_id")) if pd.notnull(row.get("curso_id")) else None

            existing = db.query(MetricaDesempenho).filter(
                MetricaDesempenho.disciplina_id == disc_id,
                MetricaDesempenho.curso_id == curso_id,
                MetricaDesempenho.ano == ano,
                MetricaDesempenho.periodo == periodo
            ).first()

            if not existing:
                metrica = MetricaDesempenho(
                    disciplina_id=disc_id,
                    curso_id=curso_id,
                    ano=ano,
                    periodo=periodo,
                    total_matriculados=int(row.get("total_matriculados", 0)),
                    aprovados=int(row.get("aprovados", 0)) if pd.notnull(row.get("aprovados")) else 0,
                    reprovados_nota=int(row.get("reprovados_nota", 0)) if pd.notnull(row.get("reprovados_nota")) else 0,
                    reprovados_falta=int(row.get("reprovados_falta", 0)) if pd.notnull(row.get("reprovados_falta")) else 0,
                    trancamentos=int(row.get("trancamentos", 0)) if pd.notnull(row.get("trancamentos")) else 0,
                    taxa_aprovacao=float(row.get("taxa_aprovacao")) if pd.notnull(row.get("taxa_aprovacao")) else None,
                    taxa_reprovacao=float(row.get("taxa_reprovacao")) if pd.notnull(row.get("taxa_reprovacao")) else None,
                    taxa_trancamento=float(row.get("taxa_trancamento")) if pd.notnull(row.get("taxa_trancamento")) else None,
                    nota_media=float(row.get("nota_media")) if pd.notnull(row.get("nota_media")) else None,
                    is_suppressed=bool(row.get("is_suppressed", False))
                )
                db.add(metrica)
                count += 1
        db.commit()
        return count
