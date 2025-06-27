import pandas as pd
import io

def load_telemetry_csv(uploaded_file) -> pd.DataFrame:
    """
    Carga un archivo CSV de telemetría ignorando encabezados inválidos y
    detectando la línea correcta del header por cantidad de columnas.
    """
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = content.splitlines()

    max_commas = 0
    header_line = 0

    for i, line in enumerate(lines):
        num_commas = line.count(",")
        if num_commas > max_commas:
            max_commas = num_commas
            header_line = i

    try:
        df = pd.read_csv(
            io.StringIO(content),
            skiprows=header_line,
            engine="python",            # usa un parser más tolerante
            on_bad_lines="skip"         # ignora filas mal formateadas
        )
    except Exception as e:
        raise ValueError(f"Error al leer CSV: {str(e)}")

    return df
