# 🏁 PitData – Dashboard de Telemetría Automovilística

**PitData** es una app web construida con **Streamlit** que permite cargar archivos `.csv` de telemetría de simuladores como Assetto Corsa o data loggers reales, para visualizar datos como velocidad, RPM, fuerzas G y comparaciones por vuelta.

---

## 🚀 ¿Qué hace la app?

- 📈 Gráficos de velocidad y RPM vs tiempo
- 🌀 Análisis de fuerzas G laterales y longitudinales
- 🛣️ Comparación de vueltas seleccionadas
- 📊 Estadísticas básicas de la sesión

---

## 🧪 Probar la app

Podés usar el archivo de ejemplo incluido en `/data/example.csv` para probar el funcionamiento.

1. Abrí la app desde [streamlit.app](https://pitdata-XXXX.streamlit.app) *(reemplazar con el link final)*
2. Subí un archivo `.csv` limpio o el `example.csv`
3. ¡Explorá tu telemetría!

---

## 🛠️ Requisitos

- Python 3.9+
- Librerías necesarias están en `requirements.txt`

Instalación local:

```bash
git clone https://github.com/TU_USUARIO/PitData.git
cd PitData
pip install -r requirements.txt
streamlit run main.py
