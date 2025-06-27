import pandas as pd
import chardet
from io import StringIO

def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    file.seek(0)
    return result['encoding']

def find_header_row(lines, min_columns=5):
    for i, line in enumerate(lines):
        columns = line.strip().split(",")
        if len(columns) >= min_columns:
            # Detectar si hay demasiadas unidades típicas (%, kg, m, s, etc.)
            if not all(col.strip().lower() in ['m', '%', 'kg', 's', 'none', ''] for col in columns):
                return i
    return 0


def load_telemetry_csv(uploaded_file):
    encoding = detect_encoding(uploaded_file)
    lines = uploaded_file.read().decode(encoding).splitlines()
    header_row = find_header_row(lines)
    try:
        df = pd.read_csv(StringIO("\n".join(lines[header_row:])), on_bad_lines='skip')
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo: {e}")
    return df

