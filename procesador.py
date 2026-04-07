import json
import time
import requests
import psycopg2
from confluent_kafka import Consumer

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================

# Configuración de Kafka
kafka_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo_procesadores_iot',
    'auto.offset.reset': 'earliest'
}

# Configuración de PostgreSQL
db_conf = {
    "host": "localhost",
    "port": "5432",
    "database": "sensores",
    "user": "admin",
    "password": "supersecreto"
}

# ==========================================
# 2. FUNCIONES DE APOYO
# ==========================================

def enviar_alerta_critica(datos):
    """
    Simula el envío de una alerta. En un entorno real, aquí conectarías
    con la API de Telegram, Slack o un servicio de Email.
    """
    print("\n" + "!" * 50)
    print(f" 🔥 [ALERTA CRÍTICA DETECTADA] 🔥")
    print(f" SENSOR: {datos['sensor_id']}")
    print(f" VALORES: Temp: {datos['temperatura']}°C | Presión: {datos['presion']} PSI")
    print(f" HORA: {datos['timestamp']}")
    print("!" * 50 + "\n")
    
    # Ejemplo de cómo sería un envío real a un Webhook (comentado):
    # requests.post("http://tu-webhook-url.com", json={"text": f"Fallo en {datos['sensor_id']}"})

def crear_tabla_si_no_existe(cursor):
    """Asegura que la infraestructura de datos esté lista."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lecturas (
            id SERIAL PRIMARY KEY,
            sensor_id VARCHAR(50),
            timestamp TIMESTAMP,
            temperatura FLOAT,
            presion FLOAT,
            estado VARCHAR(20)
        );
    """)
    print("✅ Conexión exitosa: Tabla 'lecturas' lista.")

# ==========================================
# 3. BUCLE PRINCIPAL (CONSUMER)
# ==========================================

def iniciar_procesador():
    # Inicializar Consumidor de Kafka
    consumer = Consumer(kafka_conf)
    consumer.subscribe(['sensores_iot'])

    try:
        # Inicializar Conexión a Base de Datos
        print("--- Iniciando Procesador de Datos Nivel Corporativo ---")
        print("Conectando a PostgreSQL...")
        conexion = psycopg2.connect(**db_conf)
        cursor = conexion.cursor()
        
        crear_tabla_si_no_existe(cursor)
        conexion.commit()

        print("🚀 Escuchando Kafka en tiempo real... (Ctrl+C para salir)")
        
        while True:
            # Poll busca mensajes en Kafka (espera 1 seg si no hay nada)
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"❌ Error de Kafka: {msg.error()}")
                continue

            # 1. Decodificar el mensaje
            payload = msg.value().decode('utf-8')
            datos = json.loads(payload)

            # 2. Persistir en la Base de Datos
            cursor.execute("""
                INSERT INTO lecturas (sensor_id, timestamp, temperatura, presion, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                datos['sensor_id'], 
                datos['timestamp'], 
                datos['temperatura'], 
                datos['presion'], 
                datos['estado']
            ))
            conexion.commit()

            # 3. Lógica de Negocio / Alertas
            if datos['estado'] == "ERROR":
                enviar_alerta_critica(datos)
            else:
                print(f"📥 Dato procesado: {datos['sensor_id']} | {datos['estado']}")

    except KeyboardInterrupt:
        print("\nTerminando procesos de forma segura...")
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
    finally:
        # Cierre seguro de recursos
        if 'conexion' in locals():
            cursor.close()
            conexion.close()
        consumer.close()
        print("🔒 Conexiones cerradas.")

if __name__ == "__main__":
    iniciar_procesador()