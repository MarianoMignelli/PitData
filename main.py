# main.py

import streamlit as st
import pandas as pd

from app.loaders import load_telemetry_csv
from app.detect import detect_column
from app.utils import clean_numeric_columns, compute_lap_times, get_fastest_and_slowest_laps
from app.plots import plot_speed_comparison, plot_delta_time

st.set_page_config(page_title="Dashboard de Telemetría", layout="wide")
st.title("🏎️ Dashboard de Telemetría Automovilística")

uploaded_file = st.file_uploader("📁 Subí tu archivo CSV", type="csv")

if uploaded_file:
    try:
        df = load_telemetry_csv(uploaded_file)

        # Detectar columnas
        tiempo = detect_column(df, ["time", "tiempo", "timestamp"])
        velocidad = detect_column(df, ["speed", "velocidad", "spd"])
        rpm = detect_column(df, ["rpm"])
        g_lat = detect_column(df, ["g_lat", "g lateral"])
        g_long = detect_column(df, ["g_long", "g longitudinal"])
        vuelta = detect_column(df, ["lap", "vuelta"])
        distancia = detect_column(df, ["lap distance", "distance"])

        # Limpiar columnas numéricas
        df = clean_numeric_columns(df, [tiempo, velocidad, rpm, g_lat, g_long, distancia])

        st.success("✅ Datos cargados exitosamente")
        st.write("### Vista previa de los datos")
        st.dataframe(df.head())

        if vuelta and tiempo:
            lap_times = compute_lap_times(df, vuelta, tiempo)
            lap_fast, lap_slow = get_fastest_and_slowest_laps(lap_times)

            st.subheader("🏁 Comparación entre Vuelta Rápida y Lenta")
            st.markdown(f"**Vuelta rápida:** {lap_fast} – {lap_times[lap_fast]:.3f}s")
            st.markdown(f"**Vuelta lenta:** {lap_slow} – {lap_times[lap_slow]:.3f}s")

            if distancia and velocidad:
                fig_speed = plot_speed_comparison(df, vuelta, velocidad, distancia, [lap_fast, lap_slow])
                st.plotly_chart(fig_speed, use_container_width=True)

            if distancia and tiempo:
                df_fast = df[df[vuelta] == lap_fast]
                df_slow = df[df[vuelta] == lap_slow]
                fig_delta = plot_delta_time(df_fast, df_slow, distancia, tiempo)
                st.plotly_chart(fig_delta, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👆 Subí un archivo para comenzar.")
