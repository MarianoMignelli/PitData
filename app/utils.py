# utils.py

import pandas as pd
import numpy as np

def clean_numeric_columns(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def compute_lap_times(df, lap_col, time_col):
    return df.groupby(lap_col)[time_col].max() - df.groupby(lap_col)[time_col].min()

def get_fastest_and_slowest_laps(lap_times):
    return lap_times.idxmin(), lap_times.idxmax()
