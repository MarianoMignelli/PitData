import pandas as pd
import io

def load_telemetry_csv(uploaded_file) -> pd.DataFrame:
    """
    Carga un archivo CSV ignorando las primeras líneas de metadatos.
    Detecta la fila real del encabezado automáticamente.
    """
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()

    header_line = None
    for i, line in enumerate(lines):
        # Detectamos una línea que tiene muchas comas (más de 5 columnas típicas)
        if line.count(",") >= 5:
            header_line = i
            break

    if header_line is None:
        raise ValueError("No se pudo detectar el encabezado del CSV.")

    df = pd.read_csv(io.StringIO(content), skiprows=header_line)
    return df
