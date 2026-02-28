# 🌦️ ETL Weatherstack - Pipeline Profesional con Dashboards

Proyecto de Minería de Datos que implementa un pipeline ETL completo para 
extraer, transformar, almacenar y visualizar datos climáticos usando la API de Weatherstack y PostgreSQL.

---

## 🎯 Objetivo

Desarrollar un proceso ETL profesional que incluya:

1. **Extract** → Obtención de datos desde API REST
2. **Transform** → Limpieza y normalización con Pandas
3. **Load** → Almacenamiento en PostgreSQL con SQLAlchemy
4. **Analyze** → Consultas y análisis histórico
5. **Visualize** → Dashboards interactivos con Streamlit

---

## 🚀 Quick Start

### 🔧 Requisitos

- Python 3.11+
- PostgreSQL
- Git

---

## ⚙️ Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu_usuario/etl-weatherstack.git
cd etl-weatherstack

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```
## 🔑 Configuración

Crear archivo .env en la raíz del proyecto:
```bash
API_KEY=tu_api_key_weatherstack
DATABASE_URL=postgresql://usuario:password@localhost:5432/clima_db
```
### ▶️ Ejecutar ETL
```bash
python scripts/extractor.py
```
#### Esto realizará:

- Extracción desde API

- Transformación con Pandas

- Carga a PostgreSQL

### Generación de logs

📊 Ejecutar Dashboards

📈 Dashboard Básico
streamlit run dashboard_basic.py

Incluye:

- Métricas generales

- Visualización simple

- Resumen por ciudad

## 🔎 Dashboard Interactivo
```bash
streamlit run dashboard_interactive.py
```
#### Incluye:

- Filtro por rango de fechas

- Selector dinámico

- Gráficos interactivos con Plotly

## 📊 Dashboard Avanzado
```bash
streamlit run dashboard_advanced.py
```
#### Incluye:

- Análisis histórico en pestañas (Tabs)

- Comparaciones temporales

- Scatter: Temperatura vs Humedad

- Métricas dinámicas

## 🗄️ Base de Datos

- PostgreSQL

- SQLAlchemy (ORM)

Alembic (Migraciones)

## 📁 Estructura del Proyecto
```
ETL-WEATHERSTACK/
│
├── data/
│   └── clima.csv
│
├── logs/
│   └── etl.log
│
├── scripts/
│   ├── database.py
│   ├── extractor.py
│   ├── init_db.py
│   ├── loader.py
│   ├── models.py
│   └── visualizador.py
│
├── clima-pitacho.db
├── create_db.py
├── dashboard_app.py
├── dashboard_interactive.py
├── dashboard_advanced.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```
## 🛠️ Tecnologías Utilizadas

-  Python 3.11

- requests

- pandas

- numpy

- matplotlib

- plotly

- streamlit

- python-dotenv

- psycopg2-binary

- SQLAlchemy

- Alembic

- PostgreSQL

- Git / GitHub

## 📚 Conceptos Aplicados

- Arquitectura ETL

- Consumo de APIs REST

- Modelado con ORM

- Migraciones de base de datos

- Dashboards interactivos

- Manejo de errores y logging

- Variables de entorno

- Buenas prácticas en proyectos de datos

👨‍💻 Autor

Yeferson Heredia
Ingeniería de Sistemas
CORHUILA



✅ Proyecto listo para entrega académica
