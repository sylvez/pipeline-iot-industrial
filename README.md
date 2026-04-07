# 🏭 Real-Time IoT Data Pipeline Industrial

## 📖 Descripción del Proyecto
Este proyecto es una arquitectura de datos de nivel corporativo diseñada para la ingesta, procesamiento y visualización de telemetría industrial en tiempo real. Simula el monitoreo de maquinaria crítica (Turbinas, Motores, Calderas) detectando anomalías y centralizando la información para la toma de decisiones.

## 🏗️ Arquitectura Técnica
El sistema utiliza un enfoque de microservicios distribuidos:
* **Ingesta de Datos:** Apache Kafka (vía Confluent) como bus de mensajes de alta disponibilidad.
* **Procesamiento en Tiempo Real:** Script Consumer en Python que procesa eventos y gestiona alertas críticas.
* **Almacenamiento:** PostgreSQL (Data Warehouse) para la persistencia de series temporales.
* **Consumo Externo:** API REST desarrollada con **FastAPI** para consultas de aplicaciones terceras.
* **Observabilidad:** Dashboard en **Grafana** para monitoreo visual en vivo.
* **Infraestructura:** Desplegado mediante contenedores con **Docker Compose**.

## 🛠️ Stack Tecnológico
* **Lenguajes:** Python 3.14+
* **Infraestructura:** Docker, Kafka, PostgreSQL.
* **Visualización:** Grafana.
* **APIs:** FastAPI, Uvicorn.
* **Librerías:** confluent-kafka, psycopg2, requests.

## 🚀 Cómo ejecutar el proyecto

1. **Levantar la infraestructura:**
   ```bash
   docker compose up -d

   Iniciar el ecosistema (Terminales separadas):

Procesador & Alertas: python procesador.py

Generador de Sensores: python generador.py

API REST: uvicorn api:app --reload

Ver resultados:

Dashboard: http://localhost:3000

API: http://localhost:8000/lecturas