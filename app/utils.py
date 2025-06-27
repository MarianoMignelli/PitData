# utils.py
import pandas as pd


def clean_numeric_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def compute_lap_times(df: pd.DataFrame, lap_col: str, time_col: str) -> dict:
    lap_times = {}
    for lap in df[lap_col].unique():
        lap_df = df[df[lap_col] == lap]
        if not lap_df.empty:
            t_min = lap_df[time_col].min()
            t_max = lap_df[time_col].max()
            lap_times[lap] = t_max - t_min
    return lap_times


def get_fastest_and_slowest_laps(lap_times: dict):
    sorted_laps = sorted(lap_times.items(), key=lambda x: x[1])
    return sorted_laps[0][0], sorted_laps[-1][0]


def compute_avg_lap(df: pd.DataFrame, lap_col: str) -> pd.DataFrame:
    return df.groupby(lap_col).mean(numeric_only=True).mean().to_frame().T


def compute_max_min(df: pd.DataFrame, column: str) -> tuple:
    return df[column].max(), df[column].mean()


def format_lap_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:.1f}"
