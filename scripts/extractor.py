#!/usr/bin/env python3
import os
import requests
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from scripts.loader import guardar_datos_en_bd
import logging

# Cargar .env correctamente
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WeatherstackExtractor:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url = os.getenv('WEATHERSTACK_BASE_URL')

        ciudades_env = os.getenv('CIUDADES')
        if not ciudades_env:
            raise ValueError("CIUDADES no fue cargado desde el .env")

        self.ciudades = ciudades_env.split(',')

        if not self.api_key:
            raise ValueError("API_KEY no configurada en .env")

    def extraer_clima(self, ciudad):
        try:
            url = f"{self.base_url}/current"
            params = {
                'access_key': self.api_key,
                'query': ciudad.strip()
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'error' in data:
                logger.error(f"Error en API para {ciudad}: {data['error']['info']}")
                return None

            logger.info(f"Datos extraídos para {ciudad}")
            return data

        except Exception as e:
            logger.error(f"Error extrayendo datos para {ciudad}: {str(e)}")
            return None

    def procesar_respuesta(self, response_data):
        try:
            current = response_data.get('current', {})
            location = response_data.get('location', {})

            return {
                'ciudad': location.get('name'),
                'pais': location.get('country'),
                'temperatura': current.get('temperature'),
                'humedad': current.get('humidity'),
                'descripcion': current.get('weather_descriptions', ['N/A'])[0],
                'fecha_extraccion': datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error procesando respuesta: {str(e)}")
            return None

    def ejecutar_extraccion(self):
        datos_extraidos = []

        logger.info(f"Iniciando extracción para {len(self.ciudades)} ciudades...")

        for ciudad in self.ciudades:
            response = self.extraer_clima(ciudad)
            if response:
                datos_procesados = self.procesar_respuesta(response)
                if datos_procesados:
                    datos_extraidos.append(datos_procesados)

        return datos_extraidos



if __name__ == "__main__":
    try:
        extractor = WeatherstackExtractor()
        datos = extractor.ejecutar_extraccion()

        if datos:
            guardar_datos_en_bd(datos)

        print("Proceso ETL completado correctamente.")

    except Exception as e:
        logger.error(f"Error en extracción: {str(e)}")