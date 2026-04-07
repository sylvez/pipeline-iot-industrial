import json
import time
import random
from datetime import datetime, timezone
from confluent_kafka import Producer  # (NUEVO) Importamos la librería

SENSORES = ["turbina_01", "compresor_02", "motor_03", "caldera_04"]

# (NUEVO) Configuración de conexión a nuestro Kafka local
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)
TOPIC = 'sensores_iot' # El nombre de nuestro "grupo de WhatsApp"

def generar_lectura(sensor_id):
    """Genera datos simulados realistas para un sensor."""
    probabilidad_fallo = random.random()
    
    if probabilidad_fallo < 0.05:  
        temp = round(random.uniform(100.0, 150.0), 2)
        presion = round(random.uniform(150.0, 200.0), 2)
        estado = "ERROR"
    elif probabilidad_fallo < 0.20: 
        temp = round(random.uniform(80.0, 99.9), 2)
        presion = round(random.uniform(120.0, 149.9), 2)
        estado = "WARNING"
    else: 
        temp = round(random.uniform(40.0, 79.9), 2)
        presion = round(random.uniform(80.0, 119.9), 2)
        estado = "OK"

    payload = {
        "sensor_id": sensor_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperatura": temp,
        "presion": presion,
        "estado": estado
    }
    return payload

def iniciar_simulacion():
    print(f"Enviando datos a Kafka (Topic: {TOPIC})... (Presiona Ctrl+C para detener)")
    try:
        while True:
            sensor_actual = random.choice(SENSORES)
            datos = generar_lectura(sensor_actual)
            
            # (NUEVO) Convertimos el diccionario a JSON y lo codificamos para el viaje
            datos_json = json.dumps(datos).encode('utf-8')
            
            # (NUEVO) Disparamos el dato hacia Kafka
            producer.produce(TOPIC, value=datos_json)
            producer.poll(0) # Esto mantiene a Kafka funcionando ligero
            
            print(f"Enviado a Kafka: {datos['sensor_id']} | Estado: {datos['estado']}")
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nDeteniendo simulación...")
    finally:
        # (NUEVO) Nos aseguramos de que no quede ningún dato atascado antes de cerrar
        producer.flush()

if __name__ == "__main__":
    iniciar_simulacion()