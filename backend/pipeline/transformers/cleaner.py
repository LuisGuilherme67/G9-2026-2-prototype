import pandas as pd
import unicodedata
import re

class DataCleaner:
    @staticmethod
    def slugify(text: str) -> str:
        """Converte strings em slugs amigáveis para URL."""
        if not text:
            return ""
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        return re.sub(r"[-\s]+", "-", text)

    def clean_subject_names(self, df: pd.DataFrame, col_name: str = "nome_disciplina") -> pd.DataFrame:
        if col_name in df.columns:
            df[col_name] = df[col_name].astype(str).str.strip().str.upper()
            df["slug"] = df[col_name].apply(self.slugify)
        return df

    def standardize_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Garante que colunas numéricas de aprovação/reprovação estejam no formato correto."""
        cols = ["total_matriculados", "aprovados", "reprovados_nota", "reprovados_falta", "trancamentos"]
        for c in cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
        return df
