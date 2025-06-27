import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_dashboard(df, cols):
    st.subheader("Visualizaciones")
    if cols["velocidad"] and cols["tiempo"]:
        fig = px.line(df, x=cols["tiempo"], y=cols["velocidad"], title="Velocidad vs Tiempo")
        st.plotly_chart(fig, use_container_width=True)

    if cols["rpm"]:
        fig = px.line(df, x=cols["tiempo"], y=cols["rpm"], title="RPM vs Tiempo")
        st.plotly_chart(fig, use_container_width=True)

    if cols["g_lateral"] and cols["g_longitudinal"]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df[cols["tiempo"]], y=df[cols["g_lateral"]], name="G Lateral"))
        fig.add_trace(go.Scatter(x=df[cols["tiempo"]], y=df[cols["g_longitudinal"]], name="G Longitudinal"))
        fig.update_layout(title="Fuerzas G", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
