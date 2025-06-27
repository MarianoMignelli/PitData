import pandas as pd
import io

def load_telemetry_csv(uploaded_file) -> pd.DataFrame:
    """
    Carga un archivo CSV de telemetría, omitiendo encabezados inválidos
    y detectando automáticamente el inicio de los datos reales.
    """
    # Leer el archivo como texto
    content = uploaded_file.read().decode("utf-8")

    # Buscar la línea que contiene los nombres de columnas reales
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "," in line and not any(c in line.lower() for c in ["session", "logger", "track", "version"]):
            header_line = i
            break
    else:
        raise ValueError("No se pudo detectar el encabezado del CSV.")

    # Leer el CSV desde la línea detectada
    df = pd.read_csv(io.StringIO(content), skiprows=header_line)
    return df
