import pandas as pd

def load_telemetry_csv(file):
    # Leer el archivo como texto
    lines = file.read().decode('utf-8').splitlines()

    # Buscar la línea que empieza con "time" para encontrar el inicio de los datos reales
    data_start_index = next((i for i, line in enumerate(lines) if line.strip().startswith("time,")), None)

    if data_start_index is None:
        raise ValueError("No se encontró encabezado de datos en el archivo CSV.")

    # Extraer solo los datos desde la línea del encabezado hacia abajo
    csv_data = "\n".join(lines[data_start_index:])

    # Leer como CSV con pandas
    from io import StringIO
    df = pd.read_csv(StringIO(csv_data))

    return df
