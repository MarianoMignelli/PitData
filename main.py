import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.utils import load_telemetry_csv

# Configuración
st.set_page_config(page_title="PitData", layout="wide")

# Leer CSV con metadatos
def cargar_csv_telemetria(file):
    # Leer los metadatos (líneas 1 a 9)
    metadata_lines = [next(file).strip() for _ in range(9)]
    metadata = {}
    for line in metadata_lines:
        if "," in line:
            key, value = line.split(",", 1)
            metadata[key.strip()] = value.strip()

    # Saltar las siguientes 12 líneas hasta llegar a los encabezados (línea 21)
    for _ in range(12):
        next(file)

    # Cargar los datos reales desde la línea 21 (encabezados correctos)
    df = pd.read_csv(file)
    return df, metadata

# Detectar columnas
def detectar_columna(df, palabras_clave):
    for col in df.columns:
        for clave in palabras_clave:
            if clave.lower() in col.lower():
                return col
    return None

# UI
st.title("🏁 PitData - Dashboard de Telemetría")

uploaded_file = st.file_uploader("📂 Cargá un archivo CSV de telemetría", type=["csv"])
if uploaded_file:
    try:
        df, metadata = cargar_csv_telemetria(uploaded_file)

        # Mostrar metadata en sidebar
        with st.sidebar:
            st.subheader("📄 Metadata")
            for k, v in metadata.items():
                st.markdown(f"**{k}**: {v}")

        st.success("✅ Archivo cargado correctamente")
        st.dataframe(df.head())

        # Detectar columnas
        tiempo = detectar_columna(df, ["time", "tiempo", "timestamp"])
        velocidad = detectar_columna(df, ["speed", "velocidad", "spd"])
        rpm = detectar_columna(df, ["rpm"])
        g_lat = detectar_columna(df, ["g_lat", "g lateral"])
        g_long = detectar_columna(df, ["g_long", "g longitudinal"])
        vuelta = detectar_columna(df, ["lap", "vuelta"])

        # Mostrar gráficos
        st.header("📊 Visualizaciones")
        if tiempo and velocidad:
            fig1 = px.line(df, x=tiempo, y=velocidad, title="Velocidad vs Tiempo")
            st.plotly_chart(fig1, use_container_width=True)

        if tiempo and rpm:
            fig2 = px.line(df, x=tiempo, y=rpm, title="RPM vs Tiempo")
            st.plotly_chart(fig2, use_container_width=True)

        if tiempo and g_lat and g_long:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=df[tiempo], y=df[g_lat], name="G Lateral"))
            fig3.add_trace(go.Scatter(x=df[tiempo], y=df[g_long], name="G Longitudinal"))
            fig3.update_layout(title="Fuerzas G", template="plotly_dark")
            st.plotly_chart(fig3, use_container_width=True)

        if vuelta:
            st.subheader("🛣️ Comparación por vuelta")
            vueltas = df[vuelta].dropna().unique()
            seleccionadas = st.multiselect("Seleccionar vueltas", vueltas)
            if seleccionadas:
                fig4 = go.Figure()
                for v in seleccionadas:
                    mask = df[vuelta] == v
                    fig4.add_trace(go.Scatter(x=df[mask][tiempo], y=df[mask][velocidad], name=f"Vuelta {v}"))
                fig4.update_layout(title="Velocidad por vuelta", template="plotly_dark")
                st.plotly_chart(fig4, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👆 Cargá un archivo CSV para comenzar.")
