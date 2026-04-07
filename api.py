from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="IoT Sensor API")

db_conf = {
    "host": "localhost", "port": "5432",
    "database": "sensores", "user": "admin", "password": "supersecreto"
}

@app.get("/lecturas")
def obtener_lecturas(limit: int = 10):
    """Devuelve las últimas lecturas almacenadas."""
    conn = psycopg2.connect(**db_conf)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM lecturas ORDER BY timestamp DESC LIMIT %s", (limit,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

@app.get("/estado/{sensor_id}")
def obtener_estado_sensor(sensor_id: str):
    """Devuelve la última lectura de un sensor específico."""
    conn = psycopg2.connect(**db_conf)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM lecturas WHERE sensor_id = %s ORDER BY timestamp DESC LIMIT 1", (sensor_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado