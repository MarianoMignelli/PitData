import pandas as pd


def clean_numeric_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def compute_lap_times_from_column(df: pd.DataFrame, lap_col: str, lap_time_col: str) -> dict:
    """
    Usa la columna Lap Time para calcular el tiempo total de cada vuelta.
    """
    lap_times = {}
    for lap in df[lap_col].unique():
        lap_df = df[df[lap_col] == lap]
        if not lap_df.empty:
            last_valid = lap_df[lap_time_col].dropna().iloc[-1]
            lap_times[lap] = last_valid
    return lap_times


def filter_valid_laps(df: pd.DataFrame, lap_col: str, valid_col: str) -> pd.DataFrame:
    """
    Filtra las filas cuya vuelta esté marcada como válida (Lap Invalidated == 0).
    """
    valid_laps = df[df[valid_col] == 0][lap_col].unique()
    return df[df[lap_col].isin(valid_laps)]


def get_fastest_and_slowest_laps(lap_times: dict):
    sorted_laps = sorted(lap_times.items(), key=lambda x: x[1])
    return sorted_laps[0][0], sorted_laps[-1][0]


def compute_avg_lap_time(lap_times: dict) -> float:
    return sum(lap_times.values()) / len(lap_times)


def compute_max_min(df: pd.DataFrame, column: str) -> tuple:
    return df[column].mean(), df[column].max()


def format_lap_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:04.1f}"
