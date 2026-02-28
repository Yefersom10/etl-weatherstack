#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from sqlalchemy import and_
import sys

sys.path.insert(0, '.')

from scripts.database import SessionLocal
from scripts.models import Ciudad, RegistroClima

st.set_page_config(
    page_title="Dashboard Interactivo",
    page_icon="🎛️",
    layout="wide"
)

st.title("🎛️ Dashboard Interactivo - Control Total")

db = SessionLocal()

# =====================================================
# SIDEBAR CONTROLES
# =====================================================
st.sidebar.markdown("### 🔧 Controles")

# Ciudades disponibles
ciudades_disponibles = [c.nombre for c in db.query(Ciudad).all()]

ciudades_seleccionadas = st.sidebar.multiselect(
    "🏙️ Ciudades a Mostrar",
    options=ciudades_disponibles,
    default=ciudades_disponibles
)

# Rango de fechas
fecha_inicio = st.sidebar.date_input(
    "📅 Desde:",
    value=datetime.now() - timedelta(days=30) + timedelta(days=1)
)

fecha_fin = st.sidebar.date_input(
    "📅 Hasta:",
    value=datetime.now() + timedelta(days=1)
)

# Filtros de temperatura
temp_min = st.sidebar.slider("🌡️ Temp Mín (°C):", -50, 50, value=-10)
temp_max = st.sidebar.slider("🌡️ Temp Máx (°C):", -50, 50, value=40)

# =====================================================
# CONSULTA FILTRADA
# =====================================================
registros_filtrados = db.query(
    RegistroClima,
    Ciudad.nombre
).join(Ciudad).filter(
    and_(
        Ciudad.nombre.in_(ciudades_seleccionadas),
        RegistroClima.fecha_extraccion >= fecha_inicio,
        RegistroClima.fecha_extraccion <= fecha_fin,
        RegistroClima.temperatura >= temp_min,
        RegistroClima.temperatura <= temp_max
    )
).all()

# Construcción del DataFrame
data = []

for registro, ciudad_nombre in registros_filtrados:
    data.append({
        "Ciudad": ciudad_nombre,
        "Temperatura": registro.temperatura,
        "Humedad": registro.humedad,
        "Fecha": registro.fecha_extraccion
    })

df = pd.DataFrame(data) if data else pd.DataFrame()

# =====================================================
# DASHBOARD
# =====================================================
if not df.empty:

    # ---------------- KPIs ----------------
    st.markdown("### 📊 Indicadores Clave")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌡️ Temp Max", f"{df['Temperatura'].max():.1f}°C")

    with col2:
        st.metric("🌡️ Temp Min", f"{df['Temperatura'].min():.1f}°C")

    with col3:
        st.metric("🌡️ Temp Prom", f"{df['Temperatura'].mean():.1f}°C")

    with col4:
        st.metric("💧 Humedad Prom", f"{df['Humedad'].mean():.1f}%")

    st.markdown("---")

    # ---------------- Gráficas ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribución de Temperaturas")
        fig = px.box(
            df,
            x="Ciudad",
            y="Temperatura",
            color="Ciudad",
            title="Distribución por Ciudad"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Promedio de Humedad por Ciudad")
        humedad_ciudad = df.groupby("Ciudad")["Humedad"].mean().reset_index()

        fig = px.bar(
            humedad_ciudad,
            x="Ciudad",
            y="Humedad",
            color="Humedad",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------- Evolución Temporal ----------------
    st.markdown("#### 📈 Evolución Temporal")

    df["Fecha"] = pd.to_datetime(df["Fecha"])

    temp_tiempo = df.groupby(
        ["Fecha", "Ciudad"]
    )["Temperatura"].mean().reset_index()

    fig = px.line(
        temp_tiempo,
        x="Fecha",
        y="Temperatura",
        color="Ciudad",
        title="Temperatura en el Tiempo",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------- Tabla interactiva ----------------
    st.markdown("#### 📋 Datos Detallados")

    mostrar_todos = st.checkbox("Mostrar todos los registros", value=False)

    columnas_mostrar = st.multiselect(
        "Columnas a mostrar:",
        df.columns.tolist(),
        default=["Ciudad", "Temperatura", "Humedad", "Fecha"]
    )

    if mostrar_todos:
        st.dataframe(df[columnas_mostrar], use_container_width=True, height=600)
    else:
        st.dataframe(df[columnas_mostrar].head(20), use_container_width=True)

    # ---------------- Descarga CSV ----------------
    st.markdown("---")

    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇️ Descargar datos como CSV",
        data=csv,
        file_name=f"clima_datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados")

db.close()