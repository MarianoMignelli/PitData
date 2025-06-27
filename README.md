🏎️ PitData - Dashboard de Telemetría

PitData es una app web construida con Streamlit que permite a los pilotos de automovilismo cargar archivos CSV de telemetría y visualizar métricas clave de su rendimiento en pista.

🚀 Funcionalidades

✅ Carga de archivos CSV con encabezados variables (limpieza automática)

⏱️ Cálculo de vuelta rápida, lenta y promedio

📊 Visualización de velocidad y freno

🔄 Comparación entre vueltas (velocidad y delta)

🔍 Velocidad por curva (basado en distancia recorrida)

🌑 Interfaz oscura e intuitiva

📁 Estructura del Proyecto

├── app
│   ├── core.py              # Carga y limpieza del archivo CSV
│   ├── detect.py            # Detección automática de columnas
│   ├── loaders.py           # Lógica de carga desde Streamlit
│   ├── plots.py             # Gráficos interactivos (Plotly)
│   └── utils.py             # Funciones auxiliares (tiempos, formateo, etc)
├── data
│   └── example.csv          # Ejemplo limpio de archivo CSV para pruebas
├── .streamlit
│   └── config.toml          # Configuración del layout y tema
├── main.py                  # Script principal de la app
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo 📘

📦 Requisitos

Python 3.9+

Instalación local

pip install -r requirements.txt
streamlit run main.py

Recomendado para desarrollo:

Visual Studio Code

Extensión Python y Jupyter

📄 Ejemplo de archivo CSV válido

Un archivo CSV debe incluir, al menos, las siguientes columnas:

Tiempo o timestamp

Velocidad (en km/h o m/s)

Distancia o distancia recorrida por vuelta

Número de vuelta

Además, opcionalmente puede incluir columnas como RPM, G lateral, presión de freno, etc.

🌐 Hosting gratuito sugerido

Puedes desplegar la app fácilmente en:

Streamlit Community Cloud

Solo asegúrate de:

Subir este repositorio a GitHub

Tener un archivo requirements.txt

Incluir main.py en el root

Añadir un archivo CSV en /data/ como ejemplo

💡 Futuras mejoras

Login para pilotos

Comparación entre múltiples sesiones

Subida de múltiples archivos y análisis cruzado

Exportar gráficos como imágenes o PDF

Desarrollado con ❤️ por Mariano e Inimeg Analytics
