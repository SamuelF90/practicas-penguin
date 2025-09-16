# clientes.py
import requests
import random
import uuid
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

SERVER_URL = "http://127.0.0.1:8000"
POST_ENDPOINT = f"{SERVER_URL}/logs"

# Tokens para cada servicio
TOKENS = {
    "autenticacion": "token_abc123",
    "pagos": "token_def456",
    "gestion_partidos": "token_ghi789",
}

# Niveles de severidad
SEVERITIES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Mensajes de ejemplo
SAMPLE_MESSAGES = [
    "Usuario conectado correctamente",
    "Error al procesar pago: tarjeta declinada",
    "Timeout con servicio externo",
    "Cache invalidado para usuario 123",
    "No se encontró recurso solicitado",
    "Operación completada en 34ms",
    "Excepción no controlada en worker-5",
]

def make_log(service_name):
    """Genera un log individual con campos adicionales"""
    ts = datetime.now(timezone.utc).isoformat()
    severity = random.choice(SEVERITIES)
    message = random.choice(SAMPLE_MESSAGES) + " — id:" + str(uuid.uuid4())[:8]
    extra = {
        "usuario_id": random.randint(1000, 9999),
        "ip_cliente": f"192.168.1.{random.randint(1,254)}"
    }
    return {
        "fecha_hora": ts,
        "servicio": service_name,
        "severidad": severity,
        "mensaje": message,
        **extra
    }

def enviar_log_individual(service_name):
    """Envía un log individual al servidor"""
    token = TOKENS[service_name]
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    payload = make_log(service_name)
    r = requests.post(POST_ENDPOINT, json=[payload], headers=headers, timeout=10)
    return r.status_code, r.text

def enviar_bulk(service_name, n=10):
    """Envía múltiples logs en un solo request"""
    token = TOKENS[service_name]
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    payload = [make_log(service_name) for _ in range(n)]
    r = requests.post(POST_ENDPOINT, json=payload, headers=headers, timeout=10)
    return r.status_code, r.text

def stress_test(total_logs=10, concurrency=10):
    """Envía logs de forma concurrente para simular carga"""
    print(f"Stress test: {total_logs} logs, concurrencia {concurrency}")
    tasks = []
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        for _ in range(total_logs):
            svc = random.choice(list(TOKENS.keys()))
            tasks.append(ex.submit(enviar_log_individual, svc))
        aceptados = 0
        errores = 0
        for fut in as_completed(tasks):
            try:
                status, text = fut.result()
                if 200 <= status < 300:
                    aceptados += 1
                else:
                    errores += 1
            except Exception:
                errores += 1
    print(f"Finalizado. aceptados={aceptados} errores={errores}")

if __name__ == "__main__":
    # Enviamos varios logs individuales de distintos servicios
    servicios_individuales = ["pagos", "autenticacion", "gestion_partidos"]
    print("Enviando logs individuales:")
    for svc in servicios_individuales:
        print(f"Desde {svc}:")
        print(enviar_log_individual(svc))
    
    # Enviamos bulk de 10 logs desde gestion_partidos
    print("Enviando bulk (10) desde gestion_partidos:")
    print(enviar_bulk("gestion_partidos", n=10))
    
    # Stress test descomentado
    stress_test(total_logs=10, concurrency=10)






