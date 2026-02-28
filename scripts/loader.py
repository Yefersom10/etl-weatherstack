#!/usr/bin/env python3
from scripts.database import SessionLocal
from scripts.models import Ciudad, RegistroClima
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def guardar_datos_en_bd(datos):
    db = SessionLocal()

    try:
        for item in datos:

            # Buscar o crear ciudad
            ciudad = db.query(Ciudad).filter_by(
                nombre=item["ciudad"]
            ).first()

            if not ciudad:
                ciudad = Ciudad(
                    nombre=item["ciudad"]
                )
                db.add(ciudad)
                db.commit()
                db.refresh(ciudad)

            # Crear registro climático
            nuevo_registro = RegistroClima(
                temperatura=item["temperatura"],
                humedad=item["humedad"],
                fecha_extraccion=datetime.fromisoformat(item["fecha_extraccion"]),
                ciudad_id=ciudad.id
            )

            db.add(nuevo_registro)

        db.commit()
        logger.info("Datos guardados correctamente en la base de datos")

    except Exception as e:
        db.rollback()
        logger.error(f"Error guardando en BD: {str(e)}")

    finally:
        db.close()