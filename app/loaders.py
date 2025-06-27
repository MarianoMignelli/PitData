import pandas as pd
import chardet

def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    file.seek(0)
    return result["encoding"]

def load_telemetry_csv(file):
    encoding = detect_encoding(file)
    content = file.read().decode(encoding)
    lines = content.splitlines()

    # Buscar la primera línea que tiene más de 5 columnas (cabecera real)
    header_line_index = next(
        (i for i, line in enumerate(lines) if len(line.split(",")) > 5), None
    )

    if header_line_index is None:
        raise ValueError("No se encontró un encabezado válido en el CSV.")

    # Leer solo desde esa línea en adelante
    cleaned_content = "\n".join(lines[header_line_index:])
    from io import StringIO
    df = pd.read_csv(StringIO(cleaned_content))
    return df
