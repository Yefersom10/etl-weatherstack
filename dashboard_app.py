#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys

sys.path.insert(0, '.')

from scripts.database import SessionLocal
from scripts.models import Ciudad, RegistroClima

# -----------------------------
# Configuración de la página
# -----------------------------
st.set_page_config(
    page_title="Dashboard de Clima ETL",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌍 Dashboard de Clima - ETL Weatherstack")
st.markdown("---")

# -----------------------------
# Conexión a la base de datos
# -----------------------------
db = SessionLocal()

try:
    # Consulta con join
    registros = db.query(
        RegistroClima,
        Ciudad.nombre
    ).join(
        Ciudad
    ).order_by(
        RegistroClima.fecha_extraccion.desc()
    ).all()

    # Convertir a lista de diccionarios
    data = []
    for registro, ciudad_nombre in registros:
        data.append({
    "Ciudad": ciudad_nombre,
    "Temperatura": registro.temperatura,
    "Humedad": registro.humedad,
    "Fecha": registro.fecha_extraccion
    })

    # Crear DataFrame
    df = pd.DataFrame(data)
    df["Fecha"] = pd.to_datetime(df["Fecha"]) + pd.Timedelta(days=1)

    if df.empty:
        st.warning("⚠ No hay datos en la base de datos.")
        st.stop()

    # -----------------------------
    # Sidebar filtros
    # -----------------------------
    st.sidebar.title("🔧 Filtros")

    ciudades_filtro = st.sidebar.multiselect(
        "Selecciona Ciudades:",
        options=df["Ciudad"].unique(),
        default=df["Ciudad"].unique()
    )

    df_filtrado = df[df["Ciudad"].isin(ciudades_filtro)]

    # -----------------------------
    # Métricas principales
    # -----------------------------
    st.subheader("📈 Métricas Principales")

    col1, col2, col3 = st.columns(3)

    with col1:
        temp_promedio = df_filtrado["Temperatura"].mean()
        st.metric(
            "🌡️ Temp. Promedio",
            f"{temp_promedio:.1f} °C"
        )

    with col2:
        humedad_promedio = df_filtrado["Humedad"].mean()
        st.metric(
            "💧 Humedad Promedio",
            f"{humedad_promedio:.1f} %"
        )

    with col3:
        total_registros = len(df_filtrado)
        st.metric(
            "📊 Total Registros",
            total_registros
        )

    st.markdown("---")

    # -----------------------------
    # Visualizaciones
    # -----------------------------
    st.subheader("📊 Visualizaciones")

    col1, col2 = st.columns(2)

    # Temperatura por ciudad
    with col1:
        fig_temp = px.bar(
            df_filtrado.sort_values("Temperatura", ascending=False),
            x="Ciudad",
            y="Temperatura",
            title="Temperatura por Ciudad",
            color="Temperatura",
            color_continuous_scale="RdYlBu_r"
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    # Humedad por ciudad
    with col2:
        fig_hum = px.bar(
            df_filtrado,
            x="Ciudad",
            y="Humedad",
            title="Humedad por Ciudad",
            color="Humedad",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_hum, use_container_width=True)

    # Scatter Temperatura vs Humedad
    st.subheader("🌡️ Temperatura vs Humedad")

    fig_scatter = px.scatter(
    df,
    x="Temperatura",
    y="Humedad",
    color="Ciudad"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Tabla detallada
    # -----------------------------
    st.subheader("📋 Datos Detallados")

    st.dataframe(
        df_filtrado.sort_values("Fecha", ascending=False),
        use_container_width=True,
        height=400
    )

finally:
    db.close()