import pandas as pd
from app.domain.anonymizer import hash_identifier

class PipelineAnonymizer:
    def __init__(self, k_threshold: int = 5, salt: str = "unb_tamburetei_mds_2026"):
        self.k_threshold = k_threshold
        self.salt = salt

    def mask_student_identifiers(self, df: pd.DataFrame, id_column: str = "matricula") -> pd.DataFrame:
        """Substitui a matrícula real pelo hash SHA-256 irreversível."""
        if id_column in df.columns:
            df[id_column] = df[id_column].astype(str).apply(lambda x: hash_identifier(x, self.salt))
            df.rename(columns={id_column: "id_anonimizado"}, inplace=True)
        return df

    def apply_k_anonymity_suppression(self, df: pd.DataFrame, count_col: str = "total_matriculados") -> pd.DataFrame:
        """Marca e suprime linhas onde a contagem de discentes é inferior ao limite k."""
        if count_col in df.columns:
            df["is_suppressed"] = df[count_col] < self.k_threshold
            # Para registros suprimidos, zera ou anula dados sensíveis
            sensitive_cols = ["nota_media", "aprovados", "reprovados_nota", "reprovados_falta", "trancamentos"]
            for col in sensitive_cols:
                if col in df.columns:
                    df.loc[df["is_suppressed"], col] = None
        return df
