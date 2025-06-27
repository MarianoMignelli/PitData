import pandas as pd
import chardet
from io import StringIO

def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    file.seek(0)
    return result["encoding"]

def load_telemetry_csv(file):
    encoding = detect_encoding(file)
    content = file.read().decode(encoding)
    lines = content.splitlines()

    # Detectar la línea de encabezado real
    header_line_index = next(
        (i for i, line in enumerate(lines) if len(line.split(",")) >= 10 and not all(c in ['%', 'kg', 'm', ''] for c in line.split(","))),
        None
    )

    if header_line_index is None:
        raise ValueError("No se encontró un encabezado válido en el CSV.")

    cleaned_content = "\n".join(lines[header_line_index:])

    # Cargar el DataFrame ignorando filas malformadas
    df = pd.read_csv(StringIO(cleaned_content), on_bad_lines='skip')
    return df

