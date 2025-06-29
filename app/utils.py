import pandas as pd

def clean_numeric_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def filter_valid_laps(df: pd.DataFrame, invalid_col: str) -> pd.DataFrame:
    if invalid_col in df.columns:
        return df[df[invalid_col] == 0].copy()
    return df

def get_lap_time_dict(df: pd.DataFrame, lap_col: str, lap_time_col: str) -> dict:
    lap_times = df.groupby(lap_col)[lap_time_col].max()
    return lap_times.to_dict()

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
    return f"{minutes}.{remaining_seconds:04.1f}"
