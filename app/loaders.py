import pandas as pd
import chardet

def detect_encoding(file):
    raw_data = file.read(10000)
    file.seek(0)
    return chardet.detect(raw_data)['encoding']

def load_telemetry_csv(uploaded_file):
    encoding = detect_encoding(uploaded_file)
    uploaded_file.seek(0)
    
    # Leer todas las líneas para detectar encabezado
    lines = uploaded_file.readlines()
    uploaded_file.seek(0)
    
    header_row_index = None
    for i, line in enumerate(lines):
        decoded = line.decode(encoding).lower()
        if decoded.startswith("time,"):
            header_row_index = i
            break
    
    if header_row_index is None:
        raise ValueError("No se encontró encabezado de datos (línea con 'time,') en el archivo.")
    
    # Releer el archivo como si fuera texto a partir del header
    from io import StringIO
    content = b"".join(lines[header_row_index:]).decode(encoding)
    df = pd.read_csv(StringIO(content), on_bad_lines="skip")
    
    return df
