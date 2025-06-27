# plots.py

import plotly.graph_objects as go
import pandas as pd


def plot_speed_line(df: pd.DataFrame, lap_col: str, speed_col: str, distance_col: str, selected_lap: str) -> go.Figure:
    fig = go.Figure()
    lap_df = df[df[lap_col] == selected_lap]
    fig.add_trace(go.Scatter(
        x=lap_df[distance_col],
        y=lap_df[speed_col],
        mode="lines",
        name=f"Vuelta {selected_lap}",
        line=dict(width=2)
    ))
    fig.update_layout(
        title=f"Velocidad en Vuelta {selected_lap}",
        xaxis_title="Distancia (m)",
        yaxis_title="Velocidad (km/h)",
        template="plotly_dark"
    )
    return fig


def plot_brake_line(df: pd.DataFrame, lap_col: str, brake_col: str, distance_col: str, selected_lap: str) -> go.Figure:
    fig = go.Figure()
    lap_df = df[df[lap_col] == selected_lap]
    fig.add_trace(go.Scatter(
        x=lap_df[distance_col],
        y=lap_df[brake_col],
        mode="lines",
        name=f"Freno - Vuelta {selected_lap}",
        line=dict(width=2, color="red")
    ))
    fig.update_layout(
        title=f"Freno en Vuelta {selected_lap}",
        xaxis_title="Distancia (m)",
        yaxis_title="Freno (intensidad)",
        template="plotly_dark"
    )
    return fig


def plot_corner_speed(df: pd.DataFrame, lap_col: str, speed_col: str, distance_col: str, selected_lap: str) -> go.Figure:
    lap_df = df[df[lap_col] == selected_lap].copy()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lap_df[distance_col],
        y=lap_df[speed_col],
        mode="lines+markers",
        marker=dict(size=4),
        name=f"Vuelta {selected_lap}",
    ))
    fig.update_layout(
        title="Velocidad por Curva",
        xaxis_title="Distancia (m)",
        yaxis_title="Velocidad (km/h)",
        template="plotly_dark"
    )
    return fig


def plot_speed_comparison(df: pd.DataFrame, lap_col: str, speed_col: str, distance_col: str, laps: list) -> go.Figure:
    fig = go.Figure()
    for lap in laps:
        lap_df = df[df[lap_col] == lap]
        fig.add_trace(go.Scatter(
            x=lap_df[distance_col],
            y=lap_df[speed_col],
            mode="lines",
            name=f"Vuelta {lap}" if isinstance(lap, int) else lap,
            line=dict(width=2)
        ))
    fig.update_layout(
        title="Comparación de Velocidad",
        xaxis_title="Distancia (m)",
        yaxis_title="Velocidad (km/h)",
        template="plotly_dark"
    )
    return fig


def plot_delta_time(df_fast: pd.DataFrame, df_sel: pd.DataFrame, distance_col: str, time_col: str) -> go.Figure:
    # Alinear por distancia
    merged = pd.merge(df_fast[[distance_col, time_col]],
                      df_sel[[distance_col, time_col]],
                      on=distance_col,
                      how="inner",
                      suffixes=("_fast", "_sel"))

    merged["delta"] = merged[time_col + "_sel"] - merged[time_col + "_fast"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=merged[distance_col],
        y=merged["delta"],
        mode="lines",
        name="Delta",
        line=dict(color="orange", width=2)
    ))
    fig.update_layout(
        title="Delta de Tiempo entre Vueltas",
        xaxis_title="Distancia (m)",
        yaxis_title="Diferencia de Tiempo (s)",
        template="plotly_dark"
    )
    return fig
