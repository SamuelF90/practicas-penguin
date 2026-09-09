from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import sqlite3

DB = "inventario.db"
app = FastAPI(title="Servicio de Inventario")

class Cantidad(BaseModel):
    cantidad: int

# Inicializar base de datos
def iniciar_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS stock (
        producto_id INTEGER PRIMARY KEY,
        cantidad INTEGER
    )""")
    conn.commit()
    conn.close()

iniciar_db()

def validar_token(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, detail="Token faltante o inválido")

@app.get("/stock/{id_producto}")
def ver_stock(id_producto: int, authorization: Optional[str] = Header(None)):
    validar_token(authorization)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    fila = cur.execute("SELECT cantidad FROM stock WHERE producto_id=?", (id_producto,)).fetchone()
    conn.close()
    return {"producto_id": id_producto, "stock": fila[0] if fila else 0}

@app.post("/stock/{id_producto}/disminuir")
def disminuir_stock(id_producto: int, cantidad: Cantidad, authorization: Optional[str] = Header(None)):
    validar_token(authorization)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    fila = cur.execute("SELECT cantidad FROM stock WHERE producto_id=?", (id_producto,)).fetchone()
    actual = fila[0] if fila else 0
    if actual < cantidad.cantidad:
        conn.close()
        raise HTTPException(400, detail="Stock insuficiente")
    nuevo = actual - cantidad.cantidad
    cur.execute("UPDATE stock SET cantidad=? WHERE producto_id=?", (nuevo, id_producto))
    conn.commit()
    conn.close()
    return {"producto_id": id_producto, "stock": nuevo}
