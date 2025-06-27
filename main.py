# main.py

# main.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.loaders import load_telemetry_csv
from app.detect import detect_column

st.set_page_config(page_title="Dashboard de Telemetría", layout="wide")
st.title("🏎️ Dashboard de Telemetría Automovilística")

uploaded_file = st.file_uploader("Subí tu archivo CSV", type=["csv"])

if uploaded_file:
    try:
        df = load_telemetry_csv(uploaded_file)

        # Detectar columnas claves
        tiempo_col = detect_column(df, ["time", "tiempo", "timestamp"])
        velocidad_col = detect_column(df, ["speed", "velocidad", "spd"])
        rpm_col = detect_column(df, ["rpm"])
        g_lat_col = detect_column(df, ["g_lat", "g lateral"])
        g_long_col = detect_column(df, ["g_long", "g longitudinal"])
        vuelta_col = detect_column(df, ["lap", "vuelta"])

        if not vuelta_col or not tiempo_col:
            st.error("No se encontraron las columnas necesarias para identificar vueltas o tiempo.")
            st.stop()

        # Intentar convertir la columna de tiempo a numérico
        try:
            df[tiempo_col] = pd.to_numeric(df[tiempo_col], errors="coerce")
        except Exception as e:
            st.error(f"Error convirtiendo tiempo a número: {e}")
            st.stop()

        # Calcular tiempo total por vuelta
        tiempo_total_por_vuelta = df.groupby(vuelta_col)[tiempo_col].agg(lambda x: x.max() - x.min())
        tiempo_total_por_vuelta = tiempo_total_por_vuelta.sort_values()

        # Selector de vuelta
        st.subheader("🎯 Selección de vuelta a analizar")
        vuelta_seleccionada = st.selectbox("Selecciona una vuelta", tiempo_total_por_vuelta.index,
                                           format_func=lambda x: f"Vuelta {x} – {tiempo_total_por_vuelta[x]:.2f}s")

        df_vuelta = df[df[vuelta_col] == vuelta_seleccionada]

        st.success("✅ Vuelta seleccionada correctamente")

        st.subheader("📊 Telemetría de la vuelta seleccionada")

        if tiempo_col and velocidad_col:
            fig = px.line(df_vuelta, x=tiempo_col, y=velocidad_col, title="Velocidad vs Tiempo")
            st.plotly_chart(fig, use_container_width=True)

        if tiempo_col and rpm_col:
            fig = px.line(df_vuelta, x=tiempo_col, y=rpm_col, title="RPM vs Tiempo")
            st.plotly_chart(fig, use_container_width=True)

        if tiempo_col and g_lat_col and g_long_col:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_vuelta[tiempo_col], y=df_vuelta[g_lat_col], name="G Lateral"))
            fig.add_trace(go.Scatter(x=df_vuelta[tiempo_col], y=df_vuelta[g_long_col], name="G Longitudinal"))
            fig.update_layout(title="Fuerzas G", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📈 Velocidad promedio")
        velocidad_promedio = df.groupby(vuelta_col)[velocidad_col].mean()
        st.metric(label=f"Velocidad promedio vuelta {vuelta_seleccionada}", value=f"{velocidad_promedio[vuelta_seleccionada]:.2f} km/h")

        st.subheader("🏁 Comparación de sectores (estimados)")
        try:
            df_vuelta_sorted = df_vuelta.sort_values(by=tiempo_col).reset_index(drop=True)
            df_vuelta_sorted["sector"] = pd.qcut(df_vuelta_sorted.index, q=3, labels=["Sector 1", "Sector 2", "Sector 3"])
            sector_times = df_vuelta_sorted.groupby("sector")[tiempo_col].agg(lambda x: x.max() - x.min())
            st.dataframe(sector_times.rename("Duración (s)"))
        except Exception as e:
            st.warning(f"No se pudo calcular la comparación de sectores: {e}")

        st.subheader("🌀 Velocidad por curva (estimado)")
        try:
            # Detectar zonas de frenado como 'curvas' simples por velocidad mínima
            curvas = df_vuelta_sorted[df_vuelta_sorted[velocidad_col] < df_vuelta_sorted[velocidad_col].quantile(0.2)]
            curvas = curvas.groupby(curvas.index // 20)[velocidad_col].min().reset_index(drop=True)
            fig = px.bar(curvas, y=velocidad_col, title="Velocidad mínima por curva estimada")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo estimar velocidad por curva: {e}")

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👆 Subí un archivo para comenzar.")
