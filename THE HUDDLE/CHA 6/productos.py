from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import sqlite3

DB = "productos.db"
app = FastAPI(title="Servicio de Productos")

# Modelo de producto
class Producto(BaseModel):
    nombre: str
    precio: float
    sku: Optional[str] = None

# Inicializar base de datos
def iniciar_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        sku TEXT
    )""")
    conn.commit()
    conn.close()

iniciar_db()

# Función de autenticación
def validar_token(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, detail="Token faltante o inválido")

# Rutas
@app.get("/productos")
def listar_productos(authorization: Optional[str] = Header(None)):
    validar_token(authorization)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    filas = cur.execute("SELECT id,nombre,precio,sku FROM productos").fetchall()
    conn.close()
    return [{"id": f[0], "nombre": f[1], "precio": f[2], "sku": f[3]} for f in filas]

@app.post("/productos")
def crear_producto(producto: Producto, authorization: Optional[str] = Header(None)):
    validar_token(authorization)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO productos (nombre,precio,sku) VALUES (?,?,?)",
                (producto.nombre, producto.precio, producto.sku))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return {"id": pid, "nombre": producto.nombre, "precio": producto.precio, "sku": producto.sku}
