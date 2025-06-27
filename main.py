import streamlit as st
import pandas as pd

from app.loaders import load_telemetry_csv
from app.detect import detect_column
from app.utils import clean_numeric_columns, compute_lap_times, compute_avg_lap, get_fastest_and_slowest_laps, compute_max_min, format_lap_time
from app.plots import plot_speed_line, plot_brake_line, plot_corner_speed, plot_speed_comparison, plot_delta_time

st.set_page_config(page_title="PitData", layout="wide")
st.title("🏎️ Lee tu telemetría con Nosotros")

uploaded_file = st.file_uploader("📁 Subí tu archivo CSV", type="csv")

if uploaded_file:
    try:
        df = load_telemetry_csv(uploaded_file)

        # Detectar columnas clave
        tiempo = detect_column(df, ["lap time", "laptime"])
        velocidad = detect_column(df, ["ground speed", "speed", "velocidad", "spd"])
        rpm = detect_column(df, ["rpm"])
        g_lat = detect_column(df, ["g_lat", "g lateral"])
        g_long = detect_column(df, ["g_long", "g longitudinal"])
        vuelta = detect_column(df, ["lap", "vuelta"])
        distancia = detect_column(df, ["lap distance", "distance"])
        freno = detect_column(df, ["brake", "freno"])

        # Limpiar columnas numéricas
        df = clean_numeric_columns(df, [tiempo, velocidad, rpm, g_lat, g_long, distancia, freno])

        st.success("✅ Datos cargados correctamente")

         # Calcular tiempos de vuelta
        lap_times = compute_lap_times(df, vuelta, tiempo)

        # Filtrar vueltas válidas (entre 60s y 200s por ejemplo)
        lap_times_valid = {k: v for k, v in lap_times.items() if 60 <= v <= 200}
        valid_laps = list(lap_times_valid.keys())

        # Recalcular datos con vueltas válidas
        lap_fast, lap_slow = get_fastest_and_slowest_laps(lap_times_valid)
        delta_fast_slow = lap_times_valid[lap_slow] - lap_times_valid[lap_fast]

        df_valid = df[df[vuelta].isin(valid_laps)]

        # Calcular promedio
        lap_avg = sum(lap_times_valid.values()) / len(lap_times_valid)
        v_avg, v_max = compute_max_min(df_valid, velocidad)


        # Velocidad promedio y máxima
        v_avg, v_max = compute_max_min(df, velocidad)

        # Mostrar métricas
        st.markdown("### 📊 Resumen")
        col1, col2, col3 = st.columns(3)
        col1.metric("Vuelta Rápida", format_lap_time(lap_times[lap_fast]), f"Vuelta {lap_fast}")
        col2.metric("Vuelta Lenta", format_lap_time(lap_times[lap_slow]), f"Vuelta {lap_slow}")
        col3.metric("Delta entre vueltas", f"{delta_fast_slow:.2f}s")

        col4, col5, col6 = st.columns(3)
        col4.metric("Tiempo promedio", f"{lap_avg:.2f}s")
        col5.metric("Velocidad promedio", f"{v_avg:.1f} km/h")
        col6.metric("Velocidad máxima", f"{v_max:.1f} km/h")

        # Selector de vuelta
        vuelta_sel = st.selectbox(
            "📍 Seleccioná una vuelta para comparar",
            sorted(lap_times.keys()),
            format_func=lambda k: f"Vuelta {k} – {lap_times[k]:.2f}s"
        )

        # Tabs
        tabs = st.tabs([
            "📈 Telemetría",
            "🛞 Freno",
            "📍 Velocidad por curva",
            "📊 Comparación rápida vs promedio",
            "⏱️ Delta de tiempo"
        ])

        with tabs[0]:
            st.subheader("Velocidad")
            st.plotly_chart(plot_speed_line(df, vuelta, velocidad, distancia, vuelta_sel), use_container_width=True)

        with tabs[1]:
            if freno:
                st.subheader("Freno")
                st.plotly_chart(plot_brake_line(df, vuelta, freno, distancia, vuelta_sel), use_container_width=True)
            else:
                st.warning("No se detectó columna de freno.")

        with tabs[2]:
            st.subheader("Velocidad por Curva")
            st.plotly_chart(plot_corner_speed(df, vuelta, velocidad, distancia, vuelta_sel), use_container_width=True)

        with tabs[3]:
            st.subheader("Comparación Vuelta Rápida vs Promedio")
            st.plotly_chart(plot_speed_comparison(df, vuelta, velocidad, distancia, [lap_fast]), use_container_width=True)

        with tabs[4]:
            st.subheader("Delta de Tiempo")
            df_fast = df[df[vuelta] == lap_fast]
            df_sel = df[df[vuelta] == vuelta_sel]
            st.plotly_chart(plot_delta_time(df_fast, df_sel, distancia, tiempo), use_container_width=True)

        with st.expander("📂 Ver datos crudos"):
            st.dataframe(df.head(100))

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👆 Subí un archivo para comenzar.")
