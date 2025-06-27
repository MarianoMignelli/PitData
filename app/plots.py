# plots.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def plot_speed_line(df: pd.DataFrame, x_col: str, y_col: str, label: str) -> go.Figure:
    fig = px.line(df, x=x_col, y=y_col, title=f"Velocidad – {label}", labels={x_col: "Distancia (m)", y_col: "Velocidad (km/h)"})
    fig.update_layout(template="plotly_dark")
    return fig


def plot_brake_line(df: pd.DataFrame, x_col: str, brake_col: str) -> go.Figure:
    fig = px.line(df, x=x_col, y=brake_col, title="Freno", labels={x_col: "Distancia (m)", brake_col: "Presión de Freno"})
    fig.update_layout(template="plotly_dark")
    return fig


def plot_corner_speed(df: pd.DataFrame, dist_col: str, speed_col: str, lap_col: str) -> go.Figure:
    fig = px.scatter(
        df,
        x=dist_col,
        y=speed_col,
        color=lap_col,
        title="Velocidad por Curva",
        labels={dist_col: "Distancia (m)", speed_col: "Velocidad (km/h)"}
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_speed_comparison(df: pd.DataFrame, lap_col: str, speed_col: str, dist_col: str, laps: list) -> go.Figure:
    fig = go.Figure()
    for lap in laps:
        mask = df[lap_col] == lap
        fig.add_trace(go.Scatter(
            x=df[mask][dist_col],
            y=df[mask][speed_col],
            mode='lines',
            name=f"Vuelta {lap}"
        ))
    fig.update_layout(
        title="Comparación de Velocidad entre Vueltas",
        xaxis_title="Distancia (m)",
        yaxis_title="Velocidad (km/h)",
        template="plotly_dark"
    )
    return fig


def plot_delta_time(df_fast: pd.DataFrame, df_slow: pd.DataFrame, dist_col: str, time_col: str) -> go.Figure:
    df_delta = pd.DataFrame()
    df_delta[dist_col] = df_fast[dist_col]
    df_delta["Delta"] = df_slow[time_col].values - df_fast[time_col].values
    fig = px.line(df_delta, x=dist_col, y="Delta", title="Delta de Tiempo (Lenta - Rápida)", labels={dist_col: "Distancia (m)", "Delta": "Tiempo (s)"})
    fig.update_layout(template="plotly_dark")
    return fig
