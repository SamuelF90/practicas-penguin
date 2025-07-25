#juego Gato x Raton
import random

DIRECCIONES = {
    'w': (-1, 0),   # arriba
    's': (1, 0),    # abajo
    'a': (0, -1),   # izquierda
    'd': (0, 1),    # derecha
    'q': (-1, -1),  # arriba-izquierda
    'e': (-1, 1),   # arriba-derecha
    'z': (1, -1),   # abajo-izquierda
    'c': (1, 1)     # abajo-derecha
}

def crear_tablero(filas, columnas):
    return [['⬜' for _ in range(columnas)] for _ in range(filas)]

def colocar_elementos(tablero, gato, raton, queso, obstaculos):
    for f in range(len(tablero)):
        for c in range(len(tablero[0])):
            tablero[f][c] = '⬜'
    tablero[gato[0]][gato[1]] = '🐱'
    tablero[raton[0]][raton[1]] = '🐭'
    tablero[queso[0]][queso[1]] = '🧀'
    for obs in obstaculos:
        tablero[obs[0]][obs[1]] = '🟥'

def imprimir_tablero(tablero):
    for fila in tablero:
        print(' '.join(fila))
    print()

def es_valido(pos, filas, columnas, obstaculos):
    f, c = pos
    return 0 <= f < filas and 0 <= c < columnas and pos not in obstaculos

def mover_jugador(pos_actual, direccion, filas, columnas, obstaculos):
    if direccion in DIRECCIONES:
        df, dc = DIRECCIONES[direccion]
        nueva_pos = (pos_actual[0] + df, pos_actual[1] + dc)
        if es_valido(nueva_pos, filas, columnas, obstaculos):
            return nueva_pos
    return pos_actual

def distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def evaluar_estado(gato, raton, queso):
    # Heurística mejorada para minimizar distancia gato-ratón y ratón-queso
    if gato == raton:
        return -1000
    if raton == queso:
        return 1000
    # Penaliza estar cerca del gato, premia acercarse al queso
    valor = -3 * distancia(gato, raton) + 2 * distancia(raton, queso)
    return valor

def minimax_ab(gato, raton, queso, profundidad, max_turno, alpha, beta, filas, columnas, obstaculos):
    if gato == raton:
        return (-1000, None)
    if raton == queso:
        return (1000, None)
    if profundidad == 0:
        return (evaluar_estado(gato, raton, queso), None)

    mejor_movimiento = None

    if max_turno:  # turno del gato (maximiza)
        max_eval = float('-inf')
        for direccion in DIRECCIONES.values():
            nueva_pos = (gato[0] + direccion[0], gato[1] + direccion[1])
            if not es_valido(nueva_pos, filas, columnas, obstaculos):
                continue
            eval, _ = minimax_ab(nueva_pos, raton, queso, profundidad - 1, False, alpha, beta, filas, columnas, obstaculos)
            if eval > max_eval:
                max_eval = eval
                mejor_movimiento = nueva_pos
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, mejor_movimiento
    else:  # turno del ratón (minimiza)
        min_eval = float('inf')
        for direccion in DIRECCIONES.values():
            nueva_pos = (raton[0] + direccion[0], raton[1] + direccion[1])
            if not es_valido(nueva_pos, filas, columnas, obstaculos):
                continue
            eval, _ = minimax_ab(gato, nueva_pos, queso, profundidad - 1, True, alpha, beta, filas, columnas, obstaculos)
            if eval < min_eval:
                min_eval = eval
                mejor_movimiento = nueva_pos
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, mejor_movimiento

def generar_obstaculos(filas, columnas, gato, raton, queso, cantidad=5):
    obstaculos = set()
    while len(obstaculos) < cantidad:
        f = random.randint(0, filas - 1)
        c = random.randint(0, columnas - 1)
        pos = (f, c)
        if pos != gato and pos != raton and pos != queso:
            obstaculos.add(pos)
    return list(obstaculos)

def juego():
    tamaño = input("¿Deseas un tablero de 5x5 o de 10x10? (5/10): ").strip()
    if tamaño == '5':
        filas, columnas = 5, 5
        gato = (4, 4)
        queso = (2, 2)
    elif tamaño == '10':
        filas, columnas = 10, 10
        gato = (9, 9)
        queso = (5, 5)
    else:
        print("Tamaño inválido. Solo se permite 5 o 10.")
        return

    raton = (0, 0)

    modo = input("¿Quieres jugar contra la computadora o contra otro jugador? (c/j): ").lower()

    if modo == 'c':
        tipo_ia = input("¿Querés ser el Gato (g) o el Ratón (r)? ").lower()
        ia_es_gato = tipo_ia == 'r'
        profundidad = 7
    else:
        ia_es_gato = None

    tablero = crear_tablero(filas, columnas)
    obstaculos = generar_obstaculos(filas, columnas, gato, raton, queso, cantidad=max(5, (filas * columnas) // 10))
    turnos = 0
    MAX_TURNOS = filas * 2

    while True:
        colocar_elementos(tablero, gato, raton, queso, obstaculos)
        imprimir_tablero(tablero)

        if gato == raton:
            print("🐱 ¡El Gato atrapó al Ratón! Fin del juego.")
            break
        if raton == queso:
            print("🐭 ¡El Ratón llegó al Queso! ¡Victoria del Ratón!")
            break
        if turnos >= MAX_TURNOS:
            print("🐭 ¡El Ratón logró escapar! Sobrevivió todos los turnos. 🏁")
            break

        if modo == 'c':
            turno_gato = (turnos % 2 == 0)
            if (ia_es_gato and turno_gato) or (not ia_es_gato and not turno_gato):
                print("🤖 Turno de la IA...")
                _, movimiento = minimax_ab(gato, raton, queso, profundidad, turno_gato, float('-inf'), float('inf'), filas, columnas, obstaculos)
                if movimiento:
                    if turno_gato:
                        gato = movimiento
                    else:
                        raton = movimiento
            else:
                jugador = "Gato" if turno_gato else "Ratón"
                print(f"🎮 Turno del jugador humano ({jugador})")
                mov = input("Movimiento (WASD + QEZC): ").lower()
                if turno_gato:
                    gato = mover_jugador(gato, mov, filas, columnas, obstaculos)
                else:
                    raton = mover_jugador(raton, mov, filas, columnas, obstaculos)
        else:
            # Modo jugador vs jugador
            jugador = "Gato" if turnos % 2 == 0 else "Ratón"
            print(f"🎮 Turno del jugador ({jugador})")
            mov = input("Movimiento (WASD + QEZC): ").lower()
            if turnos % 2 == 0:
                gato = mover_jugador(gato, mov, filas, columnas, obstaculos)
            else:
                raton = mover_jugador(raton, mov, filas, columnas, obstaculos)

        turnos += 1

if __name__ == "__main__":
    juego()
