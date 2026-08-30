import pandas as pd
from typing import Dict, Any

class INEPDataExtractor:
    """Extrator especializado para relatórios e microdados do Censo da Educação Superior (INEP/MEC)."""
    def filter_unb_data(self, df: pd.DataFrame, codigo_ies: int = 2) -> pd.DataFrame:
        """Filtra apenas registros correspondentes à UnB (Código IES = 2)."""
        if "CO_IES" in df.columns:
            return df[df["CO_IES"] == codigo_ies]
        elif "CODIGO_IES" in df.columns:
            return df[df["CODIGO_IES"] == codigo_ies]
        return df
