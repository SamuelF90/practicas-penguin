import random
import os
import copy

# Constantes para emojis y dimensiones
VACIO = "⬜"
RATON = "🐭"
GATO = "🐱"
OBSTACULO = "🟥"

FILAS = 5
COLUMNAS = 5

# Diccionario de direcciones para movimiento usando WASD
DIRECCIONES = {
    'w': (-1, 0),  # arriba
    's': (1, 0),   # abajo
    'a': (0, -1),  # izquierda
    'd': (0, 1)    # derecha
}

# 1. Crear tablero vacío
def crear_tablero():
    return [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]

# 2. Imprimir tablero en consola (limpia antes para mejor visual)
def imprimir_tablero(tablero):
    os.system('cls' if os.name == 'nt' else 'clear')
    for fila in tablero:
        print(" ".join(fila))
    print()

# 3. Colocar jugadores y obstáculos en el tablero
def colocar_jugadores(tablero, raton_pos, gato_pos, obstaculos):
    tablero[raton_pos[0]][raton_pos[1]] = RATON
    tablero[gato_pos[0]][gato_pos[1]] = GATO
    for obs in obstaculos:
        tablero[obs[0]][obs[1]] = OBSTACULO

# 3.1 Mover jugador según dirección
def mover(pos, direccion):
    return (pos[0] + direccion[0], pos[1] + direccion[1])

# 3.2 Validar que posición sea válida (dentro, no obstáculo)
def es_valido(pos, obstaculos):
    return (0 <= pos[0] < FILAS and
            0 <= pos[1] < COLUMNAS and
            pos not in obstaculos)

# 3.3 Evaluar tablero para la IA (distancia negativa entre gato y ratón)
def evaluar(raton_pos, gato_pos):
    return -((raton_pos[0] - gato_pos[0])**2 + (raton_pos[1] - gato_pos[1])**2)

# 3.4 Algoritmo Minimax con profundidad limitada
def minimax(tablero, raton_pos, gato_pos, profundidad, es_turno_raton, obstaculos):
    if profundidad == 0 or raton_pos == gato_pos:
        return evaluar(raton_pos, gato_pos)

    if es_turno_raton:
        mejor_valor = float('-inf')
        for d in DIRECCIONES.values():
            nueva_pos = mover(raton_pos, d)
            if es_valido(nueva_pos, obstaculos) and nueva_pos != gato_pos:
                valor = minimax(tablero, nueva_pos, gato_pos, profundidad - 1, False, obstaculos)
                mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for d in DIRECCIONES.values():
            nueva_pos = mover(gato_pos, d)
            if es_valido(nueva_pos, obstaculos) and nueva_pos != raton_pos:
                valor = minimax(tablero, raton_pos, nueva_pos, profundidad - 1, True, obstaculos)
                mejor_valor = min(mejor_valor, valor)
        return mejor_valor

# Obtener mejor movimiento para IA
def obtener_mejor_movimiento(tablero, jugador_pos, enemigo_pos, profundidad, es_turno_raton, obstaculos):
    mejor_valor = float('-inf') if es_turno_raton else float('inf')
    mejor_mov = jugador_pos

    for d in DIRECCIONES.values():
        nueva = mover(jugador_pos, d)
        if es_valido(nueva, obstaculos) and nueva != enemigo_pos:
            valor = minimax(tablero,
                            nueva if es_turno_raton else jugador_pos,
                            jugador_pos if es_turno_raton else nueva,
                            profundidad - 1,
                            not es_turno_raton,
                            obstaculos)
            if (es_turno_raton and valor > mejor_valor) or (not es_turno_raton and valor < mejor_valor):
                mejor_valor = valor
                mejor_mov = nueva
    return mejor_mov

# ✅ Leer movimiento usando WASD en consola
def leer_movimiento():
    while True:
        mov = input("Usa WASD para moverte: ").lower()
        if mov in DIRECCIONES:
            return DIRECCIONES[mov]
        else:
            print("Entrada inválida, usa solo W, A, S o D")

# Función principal del juego
def jugar():
    tablero = crear_tablero()
    raton_pos = (0, 0)
    gato_pos = (4, 4)
    obstaculos = [(2, 2), (1, 3), (3, 1)]

    modo = input("¿Querés jugar contra la computadora (c) o contra otro jugador (j)? ").lower()
    rol = input("¿Querés ser el Gato (g) o el Ratón (r)? ").lower() if modo == 'c' else None
    turno_raton = True

    while True:
        tablero_actual = crear_tablero()
        colocar_jugadores(tablero_actual, raton_pos, gato_pos, obstaculos)
        imprimir_tablero(tablero_actual)

        if raton_pos == gato_pos:
            print(f"¡{GATO} atrapó al {RATON}! Fin del juego.")
            break

        jugador_humano = modo == 'j' or (modo == 'c' and ((turno_raton and rol == 'r') or (not turno_raton and rol == 'g')))
        jugador = 'Ratón' if turno_raton else 'Gato'

        if jugador_humano:
            print(f"Turno del {jugador} (Jugador)")
            movimiento = leer_movimiento()
            nueva_pos = mover(raton_pos if turno_raton else gato_pos, movimiento)
            if es_valido(nueva_pos, obstaculos):
                if turno_raton:
                    raton_pos = nueva_pos
                else:
                    gato_pos = nueva_pos
            else:
                print("Movimiento inválido, posición fuera de rango o con obstáculo.")
        else:
            print(f"Turno del {jugador} (IA)")
            if turno_raton:
                raton_pos = obtener_mejor_movimiento(tablero_actual, raton_pos, gato_pos, 2, True, obstaculos)
            else:
                gato_pos = obtener_mejor_movimiento(tablero_actual, gato_pos, raton_pos, 2, False, obstaculos)

        turno_raton = not turno_raton

if __name__ == "__main__":
    jugar()





