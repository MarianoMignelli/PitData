import pandas as pd
from app.utils import detect_column

def load_and_prepare_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        column_mappings = {
            "tiempo": detect_column(df, ["time", "tiempo", "timestamp"]),
            "velocidad": detect_column(df, ["speed", "velocidad", "spd"]),
            "rpm": detect_column(df, ["rpm"]),
            "g_lateral": detect_column(df, ["g_lat", "g lateral"]),
            "g_longitudinal": detect_column(df, ["g_long", "g longitudinal"]),
            "vuelta": detect_column(df, ["lap", "vuelta"]),
        }
        return df, column_mappings
    except Exception:
        return None, None
