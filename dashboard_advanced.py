#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from sqlalchemy import func
import sys

sys.path.insert(0, '.')

from scripts.database import SessionLocal
from scripts.models import Ciudad, RegistroClima, MetricasETL

# ---------------------------------------------------
# Configuración
# ---------------------------------------------------
st.set_page_config(
    page_title="Dashboard Avanzado Clima",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌍 Dashboard Avanzado - Análisis de Clima")
st.markdown("---")

db = SessionLocal()

# ---------------------------------------------------
# Pestañas
# ---------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Vista General", "📈 Histórico", "🔍 Análisis", "📋 Métricas ETL"]
)

# ===================================================
# TAB 1 - VISTA GENERAL
# ===================================================
with tab1:
    st.subheader("Datos Generales del Sistema")

    col1, col2, col3 = st.columns(3)

    with col1:
        ciudades_count = db.query(func.count(Ciudad.id)).scalar()
        st.metric("🏙️ Ciudades", ciudades_count)

    with col2:
        registros_count = db.query(func.count(RegistroClima.id)).scalar()
        st.metric("📊 Registros Totales", registros_count)

    with col3:
        ultima_fecha = db.query(func.max(RegistroClima.fecha_extraccion)).scalar()
        if ultima_fecha:
            st.metric(
                "⏰ Última Actualización",
                ultima_fecha.strftime("%Y-%m-%d %H:%M")
            )
        else:
            st.metric("⏰ Última Actualización", "Sin datos")

    st.markdown("---")

    # Último registro por ciudad
    subquery = db.query(
        RegistroClima.ciudad_id,
        func.max(RegistroClima.fecha_extraccion).label("max_fecha")
    ).group_by(RegistroClima.ciudad_id).subquery()

    registros_actuales = db.query(
    Ciudad.nombre,
    RegistroClima.temperatura,
    RegistroClima.humedad
    ).join(RegistroClima).join(
        subquery,
        (RegistroClima.ciudad_id == subquery.c.ciudad_id) &
        (RegistroClima.fecha_extraccion == subquery.c.max_fecha)
    ).all()

    df_actual = pd.DataFrame(
    registros_actuales,
    columns=["Ciudad", "Temperatura", "Humedad"]
    )

    if not df_actual.empty:

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                df_actual,
                x="Ciudad",
                y="Temperatura",
                title="Temperatura Actual por Ciudad",
                color="Temperatura",
                color_continuous_scale="RdYlBu_r"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                df_actual,
                values="Humedad",
                names="Ciudad",
                title="Distribución de Humedad"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.dataframe(df_actual, use_container_width=True)
    else:
        st.warning("No hay datos actuales disponibles.")


# ===================================================
# TAB 2 - HISTÓRICO
# ===================================================
with tab2:
    st.subheader("Análisis Histórico")

    col1, col2 = st.columns(2)

    with col1:
        fecha_inicio = st.date_input(
            "Desde:",
            value=datetime.now() - timedelta(days=7) + timedelta(days=1)
        )

    with col2:
        fecha_fin = st.date_input(
            "Hasta:",
            value=datetime.now() + timedelta(days=1)
        )

    registros_historicos = db.query(
        RegistroClima,
        Ciudad.nombre
    ).join(Ciudad).filter(
        RegistroClima.fecha_extraccion >= fecha_inicio,
        RegistroClima.fecha_extraccion <= fecha_fin
    ).all()

    if registros_historicos:

        data = []
        for registro, ciudad_nombre in registros_historicos:
            data.append({
                "Fecha": registro.fecha_extraccion,
                "Ciudad": ciudad_nombre,
                "Temperatura": registro.temperatura,
                "Humedad": registro.humedad
            })

        df_historico = pd.DataFrame(data)

        fig = px.line(
            df_historico,
            x="Fecha",
            y="Temperatura",
            color="Ciudad",
            title="Temperatura en el Tiempo",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.dataframe(df_historico, use_container_width=True)

    else:
        st.warning("No hay datos en ese rango de fechas.")


# ===================================================
# TAB 3 - ANÁLISIS ESTADÍSTICO
# ===================================================
with tab3:
    st.subheader("Análisis Estadístico por Ciudad")

    ciudades = db.query(Ciudad).all()

    for ciudad in ciudades:
        with st.expander(f"📍 {ciudad.nombre}"):

            registros = db.query(RegistroClima).filter_by(
                ciudad_id=ciudad.id
            ).all()

            if registros:
                temps = [r.temperatura for r in registros]
                humeds = [r.humedad for r in registros]

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "🌡️ Temp Prom.",
                        f"{sum(temps)/len(temps):.1f}°C"
                    )

                with col2:
                    st.metric(
                        "💧 Humedad Prom.",
                        f"{sum(humeds)/len(humeds):.1f}%"
                    )

                with col3:
                    st.metric("📊 Registros", len(registros))

            else:
                st.info("No hay registros para esta ciudad.")


# ===================================================
# TAB 4 - MÉTRICAS ETL
# ===================================================
with tab4:
    st.subheader("Métricas de Ejecución ETL")

    metricas = db.query(MetricasETL).order_by(
        MetricasETL.fecha_ejecucion.desc()
    ).limit(20).all()

    if metricas:

        data = []
        for m in metricas:
            data.append({
                "Fecha": m.fecha_ejecucion,
                "Estado": m.estado,
                "Extraídos": m.registros_extraidos,
                "Guardados": m.registros_guardados,
                "Fallidos": m.registros_fallidos,
                "Tiempo (s)": float(m.tiempo_ejecucion_segundos)
            })

        df_metricas = pd.DataFrame(data)

        st.dataframe(df_metricas, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                df_metricas,
                x="Fecha",
                y="Guardados",
                title="Registros Guardados por Ejecución",
                color="Estado"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.scatter(
                df_metricas,
                x="Fecha",
                y="Tiempo (s)",
                size="Guardados",
                title="Duración de Ejecuciones",
                color="Estado"
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No hay métricas registradas aún.")


db.close()