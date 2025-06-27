import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_speed_line(df, lap_col, speed_col, dist_col, lap_selected):
    df_plot = df[df[lap_col] == lap_selected]
    fig = px.line(
        df_plot,
        x=dist_col,
        y=speed_col,
        title=f"Velocidad – Vuelta {lap_selected}",
        labels={dist_col: "Distancia (m)", speed_col: "Velocidad (km/h)"}
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_brake_line(df, lap_col, brake_col, dist_col, lap_selected):
    df_plot = df[df[lap_col] == lap_selected]
    fig = px.line(
        df_plot,
        x=dist_col,
        y=brake_col,
        title=f"Freno – Vuelta {lap_selected}",
        labels={dist_col: "Distancia (m)", brake_col: "Freno (%)"}
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_corner_speed(df, lap_col, speed_col, dist_col, lap_selected):
    df_plot = df[df[lap_col] == lap_selected]
    fig = px.scatter(
        df_plot,
        x=dist_col,
        y=speed_col,
        title=f"Velocidad por Curva – Vuelta {lap_selected}",
        labels={dist_col: "Distancia (m)", speed_col: "Velocidad (km/h)"},
        opacity=0.6
    )
    fig.update_layout(template="plotly_dark")
    return fig


def plot_speed_comparison(df, lap_col, speed_col, dist_col, laps_to_compare):
    fig = go.Figure()

    for lap in laps_to_compare:
        df_lap = df[df[lap_col] == lap]
        fig.add_trace(go.Scatter(
            x=df_lap[dist_col],
            y=df_lap[speed_col],
            mode="lines",
            name=f"Vuelta {lap}"
        ))

    # Calcular promedio por distancia
    avg_df = df.groupby(dist_col).mean(numeric_only=True).reset_index()
    fig.add_trace(go.Scatter(
        x=avg_df[dist_col],
        y=avg_df[speed_col],
        mode="lines",
        name="Promedio",
        line=dict(dash="dash")
    ))

    fig.update_layout(
        title="Comparación de Velocidad",
        template="plotly_dark",
        xaxis_title="Distancia (m)",
        yaxis_title="Velocidad (km/h)"
    )
    return fig


def plot_delta_time(df_fast, df_other, dist_col, time_col):
    df_merged = pd.merge(
        df_fast[[dist_col, time_col]],
        df_other[[dist_col, time_col]],
        on=dist_col,
        suffixes=("_fast", "_other")
    )
    df_merged["delta"] = df_merged[f"{time_col}_other"] - df_merged[f"{time_col}_fast"]

    fig = px.line(
        df_merged,
        x=dist_col,
        y="delta",
        title="Delta de Tiempo entre Vueltas",
        labels={dist_col: "Distancia (m)", "delta": "Delta (s)"}
    )
    fig.update_layout(template="plotly_dark")
    return fig
