#JUEGO GATO VS RATON
import os
import random

# ------------------------
# ⚙️ CONFIGURACIÓN GENERAL
# ------------------------

FILAS = 5
COLUMNAS = 5
MAX_TURNOS = 20

VACIO = "⬜"
RATON = "🐭"
GATO = "🐱"
QUESO = "🧀"
OBSTACULO = "🟥"

DIRECCIONES = {
    'w': (-1, 0),  # arriba
    's': (1, 0),   # abajo
    'a': (0, -1),  # izquierda
    'd': (0, 1),   # derecha
    'q': (-1, -1), # diagonal sup izq
    'e': (-1, 1),  # diagonal sup der
    'z': (1, -1),  # diagonal inf izq
    'c': (1, 1)    # diagonal inf der
}

# ------------------------
# 🧠 FUNCIONES BÁSICAS
# ------------------------

def crear_tablero():
    return [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]

def imprimir_tablero(tablero):
    os.system('cls' if os.name == 'nt' else 'clear')
    for fila in tablero:
        print(" ".join(fila))
    print()

def mover(pos, direccion):
    return (pos[0] + direccion[0], pos[1] + direccion[1])

def es_valido(pos, obstaculos):
    return (0 <= pos[0] < FILAS and
            0 <= pos[1] < COLUMNAS and
            pos not in obstaculos)

def colocar_elementos(tablero, raton_pos, gato_pos, queso_pos, obstaculos):
    for obs in obstaculos:
        tablero[obs[0]][obs[1]] = OBSTACULO
    tablero[queso_pos[0]][queso_pos[1]] = QUESO
    tablero[raton_pos[0]][raton_pos[1]] = RATON
    tablero[gato_pos[0]][gato_pos[1]] = GATO

def leer_movimiento():
    while True:
        tecla = input("Movimiento (WASD + QEZC para diagonales): ").lower()
        if tecla in DIRECCIONES:
            return DIRECCIONES[tecla]
        print("Movimiento inválido.")

# ------------------------
# 🎯 MINIMAX
# ------------------------

def evaluar(raton_pos, gato_pos, queso_pos):
    if raton_pos == gato_pos:
        return -1000
    if raton_pos == queso_pos:
        return 1000
    dist_gato = abs(raton_pos[0] - gato_pos[0]) + abs(raton_pos[1] - gato_pos[1])
    dist_queso = abs(raton_pos[0] - queso_pos[0]) + abs(raton_pos[1] - queso_pos[1])
    return dist_gato - dist_queso

def minimax(raton, gato, queso, obstaculos, profundidad, turno_raton):
    if profundidad == 0 or raton == gato or raton == queso:
        return evaluar(raton, gato, queso)

    movimientos = list(DIRECCIONES.values())
    mejor_valor = float('-inf') if turno_raton else float('inf')

    for mov in movimientos:
        if turno_raton:
            nueva_pos = mover(raton, mov)
            if es_valido(nueva_pos, obstaculos) and nueva_pos != gato:
                valor = minimax(nueva_pos, gato, queso, obstaculos, profundidad - 1, False)
                mejor_valor = max(mejor_valor, valor)
        else:
            nueva_pos = mover(gato, mov)
            if es_valido(nueva_pos, obstaculos) and nueva_pos != raton:
                valor = minimax(raton, nueva_pos, queso, obstaculos, profundidad - 1, True)
                mejor_valor = min(mejor_valor, valor)
    return mejor_valor

def obtener_mejor_mov(pos_actual, enemigo, queso, obstaculos, profundidad, turno_raton):
    mejor_valor = float('-inf') if turno_raton else float('inf')
    mejor_mov = pos_actual

    for mov in DIRECCIONES.values():
        nueva_pos = mover(pos_actual, mov)
        if es_valido(nueva_pos, obstaculos) and nueva_pos != enemigo:
            valor = minimax(nueva_pos if turno_raton else pos_actual,
                            enemigo if turno_raton else nueva_pos,
                            queso, obstaculos, profundidad - 1, not turno_raton)
            if (turno_raton and valor > mejor_valor) or (not turno_raton and valor < mejor_valor):
                mejor_valor = valor
                mejor_mov = nueva_pos
    return mejor_mov

# ------------------------
# 🎮 JUEGO PRINCIPAL
# ------------------------

def jugar():
    tablero = crear_tablero()
    raton_pos = (0, 0)
    gato_pos = (FILAS - 1, COLUMNAS - 1)
    queso_pos = (FILAS // 2, COLUMNAS // 2)

    # Obstáculos fijos por ahora (se pueden randomizar)
    obstaculos = [(1, 2), (2, 1), (3, 3)]

    modo = input("¿Contra computadora (c) o 2 jugadores (j)? ").lower()
    rol = input("¿Querés ser Gato (g) o Ratón (r)? ").lower() if modo == 'c' else None
    dificultad = 2
    if modo == 'c':
        try:
            dificultad = int(input("Dificultad IA (1 a 4): "))
            if not (1 <= dificultad <= 4):
                dificultad = 2
        except:
            pass

    turno_raton = True
    turnos = 0

    while turnos < MAX_TURNOS:
        tablero = crear_tablero()
        colocar_elementos(tablero, raton_pos, gato_pos, queso_pos, obstaculos)
        imprimir_tablero(tablero)

        if raton_pos == gato_pos:
            print("🐱 atrapó al 🐭. ¡Fin del juego!")
            return
        if raton_pos == queso_pos:
            print("🐭 llegó al 🧀. ¡Ganó el Ratón!")
            return

        jugador = "Ratón 🐭" if turno_raton else "Gato 🐱"
        es_humano = (modo == 'j' or
                     (modo == 'c' and rol == 'r' and turno_raton) or
                     (modo == 'c' and rol == 'g' and not turno_raton))

        print(f"Turno del {jugador} ({'Jugador' if es_humano else 'IA'})")

        if es_humano:
            movimiento = leer_movimiento()
            nueva_pos = mover(raton_pos if turno_raton else gato_pos, movimiento)
            if es_valido(nueva_pos, obstaculos):
                if turno_raton:
                    raton_pos = nueva_pos
                else:
                    gato_pos = nueva_pos
            else:
                print("Movimiento inválido.")
                continue
        else:
            if turno_raton:
                raton_pos = obtener_mejor_mov(raton_pos, gato_pos, queso_pos, obstaculos, dificultad, True)
            else:
                gato_pos = obtener_mejor_mov(gato_pos, raton_pos, queso_pos, obstaculos, dificultad, False)

        turno_raton = not turno_raton
        turnos += 1

    print("⏳ ¡Se acabaron los turnos! Empate.")

if __name__ == "__main__":
    jugar()
