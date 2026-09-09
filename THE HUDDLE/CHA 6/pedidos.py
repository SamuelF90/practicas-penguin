from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import requests

app = FastAPI(title="Servicio de Pedidos")
DB = "pedidos.db"

URL_PRODUCTOS = "http://localhost:8001"
URL_INVENTARIO = "http://localhost:8002"
URL_AUTENTICACION = "http://localhost:8000"

class Item(BaseModel):
    producto_id: int
    cantidad: int

class Pedido(BaseModel):
    usuario_id: int
    items: List[Item]

def iniciar_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        items TEXT,
        estado TEXT,
        creado_en TEXT
    )""")
    conn.commit()
    conn.close()

iniciar_db()

def obtener_token_servicio():
    resp = requests.post(f"{URL_AUTENTICACION}/token", json={"servicio":"pedido","secreto":"clave_pingüino"})
    resp.raise_for_status()
    return resp.json()["token_acceso"]

@app.post("/pedidos/crear")
def crear_pedido(pedido: Pedido, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, detail="Token de cliente faltante")
    token_servicio = obtener_token_servicio()
    headers = {"Authorization": f"Bearer {token_servicio}"}

    # Validar productos
    for item in pedido.items:
        resp = requests.get(f"{URL_PRODUCTOS}/productos/{item.producto_id}", headers=headers)
        if resp.status_code != 200:
            raise HTTPException(502, detail=f"Producto {item.producto_id} inválido")

    # Disminuir stock
    for item in pedido.items:
        resp = requests.post(f"{URL_INVENTARIO}/stock/{item.producto_id}/disminuir",
                             json={"cantidad": item.cantidad}, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(502, detail=f"No se pudo disminuir stock del producto {item.producto_id}")

    # Guardar pedido
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO pedidos (usuario_id, items, estado, creado_en) VALUES (?,?,?,datetime('now'))",
                (pedido.usuario_id, str([i.dict() for i in pedido.items]), "CONFIRMADO"))
    conn.commit()
    id_pedido = cur.lastrowid
    conn.close()
    return {"pedido_id": id_pedido, "estado": "CONFIRMADO"}
