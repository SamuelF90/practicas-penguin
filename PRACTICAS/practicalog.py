# practicalog.py
from fastapi import FastAPI, Header, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timezone

app = FastAPI(title="Logging Central - Penguin Academy", version="0.3.0")

# Tokens para cada servicio
TOKENS = {
    "autenticacion": "token_abc123",
    "pagos": "token_def456",
    "gestion_partidos": "token_ghi789",
}

# Modelo de log en español
class Log(BaseModel):
    fecha_hora: str
    servicio: str
    severidad: str
    mensaje: str
    usuario: Optional[str] = None
    id_transaccion: Optional[str] = None
    origen: Optional[str] = None
    modulo: Optional[str] = None

# 🔹 Inicializar la base de datos SQLite
def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_hora TEXT,
        servicio TEXT,
        severidad TEXT,
        mensaje TEXT,
        usuario TEXT,
        id_transaccion TEXT,
        origen TEXT,
        modulo TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def raiz():
    return {"mensaje": "Logging Central - listo"}

@app.get("/salud")
def salud():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]
    conn.close()
    return {"estado": "ok", "logs_totales": total}

@app.post("/logs")
def agregar_logs(logs: List[Log], authorization: str = Header(...)):
    # Validar token
    token_valido = any(authorization == f"Token {t}" for t in TOKENS.values())
    if not token_valido:
        raise HTTPException(status_code=401, detail="Token inválido")

    accepted = 0
    errors = []

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    for log in logs:
        try:
            cursor.execute("""
                INSERT INTO logs (fecha_hora, servicio, severidad, mensaje, usuario, id_transaccion, origen, modulo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log.fecha_hora, log.servicio, log.severidad, log.mensaje,
                log.usuario, log.id_transaccion, log.origen, log.modulo
            ))
            accepted += 1
        except Exception as e:
            errors.append(str(e))

    conn.commit()
    conn.close()

    return {"aceptados": accepted, "errores": errors}

# 🔹 Nuevo endpoint GET /logs con filtros
@app.get("/logs")
def obtener_logs(
    limit: int = 100,   # Por defecto 100 logs
    timestamp_start: Optional[str] = Query(None, description="Filtrar logs desde esta fecha (ISO 8601)"),
    timestamp_end: Optional[str] = Query(None, description="Filtrar logs hasta esta fecha (ISO 8601)"),
    severidad: Optional[str] = Query(None, description="Filtrar logs por nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    query = """
        SELECT fecha_hora, servicio, severidad, mensaje, usuario, id_transaccion, origen, modulo
        FROM logs
    """
    conditions = []
    params = []

    if timestamp_start:
        conditions.append("fecha_hora >= ?")
        params.append(timestamp_start)
    if timestamp_end:
        conditions.append("fecha_hora <= ?")
        params.append(timestamp_end)
    if severidad:
        conditions.append("severidad = ?")
        params.append(severidad)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    logs = [
        {
            "fecha_hora": row[0],
            "servicio": row[1],
            "severidad": row[2],
            "mensaje": row[3],
            "usuario": row[4],
            "id_transaccion": row[5],
            "origen": row[6],
            "modulo": row[7]
        }
        for row in rows
    ]

    return {"count": len(logs), "logs": logs}

# 🔹 Función para enviar logs desde el mismo archivo
import requests

def enviar_log(log, url, token):
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    response = requests.post(url, json=[log], headers=headers)
    return response.status_code, response.json()


# 🔹 Ejemplo de log
log_ejemplo = {
    "fecha_hora": datetime.now(timezone.utc).isoformat(),
    "servicio": "autenticacion",
    "severidad": "ERROR",
    "mensaje": "Intento fallido de login",
    "usuario": "carlos",
    "id_transaccion": None,
    "origen": "127.0.0.1",
    "modulo": "login"
}

if __name__ == "__main__":
    import uvicorn
    # 🚀 Levantar servidor
    uvicorn.run("practicalog:app", host="127.0.0.1", port=8000, reload=True)



