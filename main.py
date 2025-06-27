# main.py

import streamlit as st
from app.loaders import load_telemetry_csv
from app.detect import detect_column
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Telemetría", layout="wide")
st.title("🏎️ Dashboard de Telemetría Automovilística")

uploaded_file = st.file_uploader("Subí tu archivo CSV", type=["csv"])

if uploaded_file:
    try:
        df = load_telemetry_csv(uploaded_file)

        st.success("✅ Archivo cargado exitosamente")
        st.dataframe(df.head())

        # Detectar columnas claves
        tiempo = detect_column(df, ["time", "tiempo", "timestamp"])
        velocidad = detect_column(df, ["speed", "velocidad", "spd"])
        rpm = detect_column(df, ["rpm"])
        g_lat = detect_column(df, ["g_lat", "g lateral"])
        g_long = detect_column(df, ["g_long", "g longitudinal"])
        vuelta = detect_column(df, ["lap", "vuelta"])

        st.subheader("📊 Visualizaciones")

        if tiempo and velocidad:
            fig = px.line(df, x=tiempo, y=velocidad, title="Velocidad vs Tiempo")
            st.plotly_chart(fig, use_container_width=True)

        if tiempo and rpm:
            fig = px.line(df, x=tiempo, y=rpm, title="RPM vs Tiempo")
            st.plotly_chart(fig, use_container_width=True)

        if tiempo and g_lat and g_long:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df[tiempo], y=df[g_lat], name="G Lateral"))
            fig.add_trace(go.Scatter(x=df[tiempo], y=df[g_long], name="G Longitudinal"))
            fig.update_layout(title="Fuerzas G", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        if vuelta:
            st.subheader("🛣️ Comparación por vuelta")
            vueltas = df[vuelta].dropna().unique()
            seleccionadas = st.multiselect("Seleccionar vueltas", vueltas)
            if seleccionadas:
                fig = go.Figure()
                for v in seleccionadas:
                    mask = df[vuelta] == v
                    fig.add_trace(go.Scatter(x=df[mask][tiempo], y=df[mask][velocidad], name=f"Vuelta {v}"))
                fig.update_layout(title="Velocidad por vuelta", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👆 Subí un archivo para comenzar.")
