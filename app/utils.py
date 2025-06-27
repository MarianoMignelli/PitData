import pandas as pd

def clean_numeric_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def get_valid_laps(df: pd.DataFrame, lap_col="Lap", time_col="Time", invalid_col="Lap Invalidated") -> dict:
    """
    Devuelve un diccionario de vueltas válidas (Lap ID -> tiempo de vuelta en segundos).
    Excluye vueltas con Lap Invalidated == 1 y filtra por duración razonable.
    """
    valid_laps = {}
    for lap_id, group in df.groupby(lap_col):
        if invalid_col in group.columns and group[invalid_col].max() == 1:
            continue  # vuelta inválida
        t_min = group[time_col].min()
        t_max = group[time_col].max()
        lap_time = t_max - t_min
        if 60 <= lap_time <= 200:  # filtro de duración razonable
            valid_laps[lap_id] = lap_time
    return valid_laps

def get_fastest_and_slowest_laps(lap_times: dict):
    sorted_laps = sorted(lap_times.items(), key=lambda x: x[1])
    return sorted_laps[0][0], sorted_laps[-1][0]

def compute_max_min(df: pd.DataFrame, column: str) -> tuple:
    return df[column].mean(), df[column].max()

def format_lap_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:.1f}"
