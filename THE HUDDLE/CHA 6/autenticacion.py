from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt

app = FastAPI(title="Servicio de Autenticación")

# Configuración de JWT
CLAVE_SECRETA = "secreto_pingüino_2025"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 60

class SolicitudToken(BaseModel):
    servicio: str
    secreto: str

@app.post("/token")
def emitir_token(solicitud: SolicitudToken):
    if solicitud.secreto != "clave_pingüino":
        raise HTTPException(status_code=401, detail="Secreto inválido")
    expiracion = datetime.utcnow() + timedelta(minutes=MINUTOS_EXPIRACION)
    payload = {"sub": solicitud.servicio, "exp": expiracion.isoformat()}
    token = jwt.encode(payload, CLAVE_SECRETA, algorithm=ALGORITMO)
    return {"token_acceso": token, "tipo_token": "bearer"}

@app.post("/validar")
def validar_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(403, detail="Falta el header Authorization")
    try:
        esquema, token = authorization.split()
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        return {"valido": True, "datos": datos}
    except Exception as e:
        raise HTTPException(401, detail=str(e))
