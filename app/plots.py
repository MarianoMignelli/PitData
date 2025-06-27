# plots.py

import plotly.graph_objects as go

def plot_speed_comparison(df, lap_col, speed_col, dist_col, laps):
    fig = go.Figure()
    colors = ["lime", "red", "blue", "orange"]
    for idx, lap in enumerate(laps):
        mask = df[lap_col] == lap
        fig.add_trace(go.Scatter(
            x=df[mask][dist_col],
            y=df[mask][speed_col],
            mode='lines',
            name=f"Vuelta {lap}",
            line=dict(color=colors[idx % len(colors)])
        ))
    fig.update_layout(
        title="Comparación de Velocidad por Distancia",
        xaxis_title="Distancia (m)",
        yaxis_title="Velocidad (km/h)",
        template="plotly_dark",
        legend_title="Vuelta"
    )
    return fig


def plot_delta_time(df_fast, df_slow, dist_col, time_col):
    from numpy import interp
    ref_dist = df_fast[dist_col]
    ref_time = df_fast[time_col] - df_fast[time_col].min()
    comp_time = df_slow[time_col] - df_slow[time_col].min()
    comp_interp = interp(ref_dist, df_slow[dist_col], comp_time)
    delta = comp_interp - ref_time.values

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ref_dist,
        y=delta,
        mode='lines',
        name='Delta de Tiempo',
        line=dict(color='yellow')
    ))
    fig.update_layout(
        title="Delta de Tiempo entre Vuelta Rápida y Lenta",
        xaxis_title="Distancia (m)",
        yaxis_title="Delta Tiempo (s)",
        template="plotly_dark"
    )
    return fig
