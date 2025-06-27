# main.py

import streamlit as st
from app.core.loaders import load_telemetry_csv
from app.core.detect import detect_column
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Dashboard de Telemetría", layout="wide")
st.title("🏎️ Dashboard de Telemetría Automovilística")

uploaded_file = st.file_uploader("Subí tu archivo CSV", type=["csv"])

if uploaded_file:
    try:
        df = load_telemetry_csv(uploaded_file)
        st.success("✅ Archivo cargado exitosamente")

        # Detectar columnas claves
        tiempo = detect_column(df, ["time", "tiempo", "timestamp"])
        velocidad = detect_column(df, ["speed", "velocidad", "spd"])
        rpm = detect_column(df, ["rpm"])
        g_lat = detect_column(df, ["g_lat", "g lateral"])
        g_long = detect_column(df, ["g_long", "g longitudinal"])
        vuelta = detect_column(df, ["lap", "vuelta"])
        distancia = detect_column(df, ["lap distance", "distance"])

        if tiempo:
            df[tiempo] = pd.to_numeric(df[tiempo], errors='coerce')
        if velocidad:
            df[velocidad] = pd.to_numeric(df[velocidad], errors='coerce')
        if rpm:
            df[rpm] = pd.to_numeric(df[rpm], errors='coerce')
        if g_lat:
            df[g_lat] = pd.to_numeric(df[g_lat], errors='coerce')
        if g_long:
            df[g_long] = pd.to_numeric(df[g_long], errors='coerce')
        if distancia:
            df[distancia] = pd.to_numeric(df[distancia], errors='coerce')

        st.dataframe(df.head())

        if vuelta and tiempo:
            vueltas = df[vuelta].dropna().unique()
            tiempos_por_vuelta = df.groupby(vuelta)[tiempo].max() - df.groupby(vuelta)[tiempo].min()
            vuelta_rapida = tiempos_por_vuelta.idxmin()
            vuelta_lenta = tiempos_por_vuelta.idxmax()

            st.subheader("🏁 Comparación entre Vuelta Rápida y Lenta")
            st.markdown(f"**Vuelta más rápida:** {vuelta_rapida} - {tiempos_por_vuelta[vuelta_rapida]:.3f}s")
            st.markdown(f"**Vuelta más lenta:** {vuelta_lenta} - {tiempos_por_vuelta[vuelta_lenta]:.3f}s")

            if distancia and velocidad:
                fig = go.Figure()
                for v, label, color in zip([vuelta_rapida, vuelta_lenta], ["Rápida", "Lenta"], ["lime", "red"]):
                    mask = df[vuelta] == v
                    fig.add_trace(go.Scatter(x=df[mask][distancia], y=df[mask][velocidad], name=f"{label} (Vuelta {v})", line=dict(color=color)))
                fig.update_layout(title="Velocidad vs Distancia - Vuelta Rápida vs Lenta", xaxis_title="Distancia (m)", yaxis_title="Velocidad (km/h)", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Visualizaciones adicionales")

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
            st.subheader("🛣️ Comparación por vuelta personalizada")
            vueltas = df[vuelta].dropna().unique()
            seleccionadas = st.multiselect("Seleccionar vueltas", vueltas)
            if seleccionadas and tiempo and velocidad:
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
