import streamlit as st
from app.core import load_and_prepare_data
from app.plots import render_dashboard

st.set_page_config(page_title="Telemetría", layout="wide")
st.title("🏎️ Dashboard de Telemetría")

uploaded_file = st.file_uploader("Subí tu archivo CSV", type="csv")

if uploaded_file:
    df, cols = load_and_prepare_data(uploaded_file)
    if df is not None:
        render_dashboard(df, cols)
    else:
        st.error("No se pudo procesar el archivo.")
