from typing import List, Optional
import pandas as pd

def detect_column(df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
    """
    Busca la columna más probable del DataFrame según palabras clave.
    """
    for col in df.columns:
        col_lower = col.lower()
        for keyword in keywords:
            if keyword in col_lower:
                return col
    return None
