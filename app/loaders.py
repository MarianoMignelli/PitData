# loaders.py

import pandas as pd
import chardet

def detect_encoding(file) -> str:
    result = chardet.detect(file.read())
    file.seek(0)
    return result["encoding"]

def is_valid_header(columns):
    # Algunas palabras clave típicas en telemetría
    keywords = ['speed', 'throttle', 'brake', 'rpm', 'gear', 'lap', 'time', 'distance']
    matches = sum(1 for col in columns if any(k in col.lower() for k in keywords))
    return matches >= 3  # Consideramos válido si hay al menos 3 coincidencias

def find_header_row(lines, min_columns=5):
    for i, line in enumerate(lines):
        columns = line.strip().split(",")
        if len(columns) >= min_columns and is_valid_header(columns):
            return i
    return 0

def load_telemetry_csv(uploaded_file):
    try:
        encoding = detect_encoding(uploaded_file)
        lines = uploaded_file.read().decode(encoding).splitlines()
        header_row = find_header_row(lines)
        uploaded_file.seek(0)

        df = pd.read_csv(uploaded_file, skiprows=header_row, encoding=encoding)

        if df.empty or df.shape[1] < 2:
            raise ValueError("El archivo fue leído pero no contiene datos válidos.")
        
        return df, None
    except Exception as e:
        return None, str(e)
