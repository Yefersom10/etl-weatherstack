from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from scripts.database import Base


class Ciudad(Base):
    __tablename__ = "ciudades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais = Column(String)


class RegistroClima(Base):
    __tablename__ = "registros_clima"

    id = Column(Integer, primary_key=True, index=True)
    ciudad_id = Column(Integer, ForeignKey("ciudades.id"))
    temperatura = Column(Float)
    humedad = Column(Integer)
    fecha_extraccion = Column(DateTime, default=datetime.utcnow)

    ciudad = relationship("Ciudad")


class MetricasETL(Base):
    __tablename__ = "metricas_etl"

    id = Column(Integer, primary_key=True, index=True)
    registros_procesados = Column(Integer)
    tiempo_ejecucion = Column(Float)
    fecha_ejecucion = Column(DateTime, default=datetime.utcnow)