import pandas as pd
from typing import Optional

class CSVExtractor:
    def extract_from_csv(self, file_path: str, sep: str = ",") -> pd.DataFrame:
        """Extrai dados brutos a partir de arquivo CSV com tratamento de encoding."""
        try:
            return pd.read_csv(file_path, sep=sep, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(file_path, sep=sep, encoding="latin1")

    def extract_from_excel(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """Extrai dados a partir de planilhas XLSX da UnB/DPO."""
        return pd.read_excel(file_path, sheet_name=sheet_name or 0)
