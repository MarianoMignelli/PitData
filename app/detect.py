# detect.py

def detect_column(df, keywords):
    for col in df.columns:
        lower_col = col.lower()
        for keyword in keywords:
            if keyword.lower() in lower_col:
                return col
    return None
