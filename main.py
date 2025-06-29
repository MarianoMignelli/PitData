import streamlit as st
import pandas as pd

from app.loaders import load_telemetry_csv
from app.detect import detect_column
from app.utils import (
    clean_numeric_columns,
    filter_valid_laps,
    get_lap_time_dict,
    get_fastest_and_slowest_laps,
    compute_avg_lap_time,
    compute_max_min,
    format_lap_time
)
from app.plots import (
    plot_speed_line,
    plot_brake_line,
    plot_corner_speed,
    plot_speed_comparison,
    plot_delta_time
)

st.set_page_config(page_title="PitData", layout="wide")
st.title("🏎️ Lee tu telemetría con Nosotros")

uploaded_file = st.file_uploader("📁 Subí tu archivo CSV", type="csv")

if uploaded_file:
    try:
        df = load_telemetry_csv(uploaded_file)

        # Detectar columnas clave
        tiempo = detect_column(df, ["time", "tiempo", "timestamp"])
        velocidad = detect_column(df, ["speed", "velocidad", "spd", "ground speed"])
        rpm = detect_column(df, ["rpm"])
        g_lat = detect_column(df, ["g_lat", "g lateral"])
        g_long = detect_column(df, ["g_long", "g longitudinal"])
        vuelta = detect_column(df, ["lap", "vuelta"])
        distancia = detect_column(df, ["lap distance", "distance"])
        freno = detect_column(df, ["brake", "freno"])
        lap_time_col = detect_column(df, ["lap time"])
        invalid_col = detect_column(df, ["lap invalidated"])

        df = clean_numeric_columns(df, [tiempo, velocidad, rpm, g_lat, g_long, distancia, freno, lap_time_col])
        df_valid = filter_valid_laps(df, invalid_col)

        st.success("✅ Datos cargados correctamente")

        lap_times = get_lap_time_dict(df_valid, vuelta, lap_time_col)
        lap_avg = compute_avg_lap_time(lap_times)
        lap_fast, lap_slow = get_fastest_and_slowest_laps(lap_times)
        delta_fast_slow = lap_times[lap_slow] - lap_times[lap_fast]

        v_avg, v_max = compute_max_min(df_valid, velocidad)

        st.markdown("### 📊 Resumen")
        col1, col2, col3 = st.columns(3)
        col1.metric("Vuelta Rápida", format_lap_time(lap_times[lap_fast]), f"Vuelta {lap_fast}")
        col2.metric("Vuelta Lenta", format_lap_time(lap_times[lap_slow]), f"Vuelta {lap_slow}")
        col3.metric("Delta entre vueltas", f"{delta_fast_slow:.2f}s")

        col4, col5, col6 = st.columns(3)
        col4.metric("Tiempo promedio", f"{lap_avg:.2f}s")
        col5.metric("Velocidad promedio", f"{v_avg:.1f} km/h")
        col6.metric("Velocidad máxima", f"{v_max:.1f} km/h")

        vuelta_sel = st.selectbox(
            "📍 Seleccioná una vuelta para comparar",
            sorted(lap_times.keys()),
            format_func=lambda k: f"Vuelta {k} – {lap_times[k]:.2f}s"
        )

        tabs = st.tabs(["📈 Telemetría", "🛞 Freno", "📍 Velocidad por curva", "📊 Comparación", "⏱️ Delta de tiempo"])

        with tabs[0]:
            st.subheader("Velocidad (línea)")
            st.plotly_chart(plot_speed_line(df_valid, vuelta, velocidad, distancia, vuelta_sel), use_container_width=True)

        with tabs[1]:
            if freno:
                st.subheader("Freno (línea)")
                st.plotly_chart(plot_brake_line(df_valid, vuelta, freno, distancia, vuelta_sel), use_container_width=True)
            else:
                st.warning("No se detectó columna de freno.")

        with tabs[2]:
            st.subheader("Velocidad por Curva")
            st.plotly_chart(plot_corner_speed(df_valid, vuelta, velocidad, distancia, vuelta_sel), use_container_width=True)

        with tabs[3]:
            st.subheader("Comparación Vuelta Rápida vs Promedio")
            st.plotly_chart(plot_speed_comparison(df_valid, vuelta, velocidad, distancia, [lap_fast]), use_container_width=True)

        with tabs[4]:
            st.subheader("Delta de Tiempo entre vueltas")
            df_fast = df_valid[df_valid[vuelta] == lap_fast]
            df_sel = df_valid[df_valid[vuelta] == vuelta_sel]
            st.plotly_chart(plot_delta_time(df_fast, df_sel, distancia, tiempo), use_container_width=True)

        with st.expander("📂 Ver datos crudos"):
            st.dataframe(df_valid.head(100))

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👆 Subí un archivo para comenzar.")
