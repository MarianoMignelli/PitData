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
        if len(line.strip().split(",")) >= min_columns:
            return i
    return 0

def load_telemetry_csv(uploaded_file):
    encoding = detect_encoding(uploaded_file)
    lines = uploaded_file.read().decode(encoding).splitlines()
    header_row = find_header_row(lines)
    df = pd.read_csv(StringIO("\n".join(lines[header_row:])))
    return df
