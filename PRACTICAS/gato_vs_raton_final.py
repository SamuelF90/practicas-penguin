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
    if gato == raton:
        return -100
    if raton == queso:
        return 100
    return -distancia(gato, raton) + distancia(raton, queso)

def minimax(gato, raton, queso, profundidad, max_turno, filas, columnas, obstaculos):
    if gato == raton:
        return (-100, None)
    if raton == queso:
        return (100, None)
    if profundidad == 0:
        return (evaluar_estado(gato, raton, queso), None)

    mejor_valor = float('-inf') if max_turno else float('inf')
    mejor_movimiento = None
    jugador_actual = gato if max_turno else raton

    for direccion in DIRECCIONES.values():
        nueva_pos = (jugador_actual[0] + direccion[0], jugador_actual[1] + direccion[1])
        if not es_valido(nueva_pos, filas, columnas, obstaculos):
            continue
        nuevo_gato = nueva_pos if max_turno else gato
        nuevo_raton = nueva_pos if not max_turno else raton

        valor, _ = minimax(nuevo_gato, nuevo_raton, queso, profundidad - 1, not max_turno, filas, columnas, obstaculos)

        if max_turno:
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = nueva_pos
        else:
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = nueva_pos

    return (mejor_valor, mejor_movimiento)

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
    elif tamaño == '10':
        filas, columnas = 10, 10
        gato = (9, 9)
    else:
        print("Tamaño inválido. Solo se permite 5 o 10.")
        return

    raton = (0, 0)
    queso = (filas - 1, columnas - 1)

    modo = input("¿Quieres jugar contra la computadora o contra un jugador? (c/j): ").lower()
    tablero = crear_tablero(filas, columnas)
    obstaculos = generar_obstaculos(filas, columnas, gato, raton, queso, cantidad=max(5, (filas * columnas) // 10))
    profundidad = 3

    if modo == 'c':
        tipo_ia = input("¿Querés ser el Gato (g) o el Ratón (r)? ").lower()
        ia_es_gato = tipo_ia == 'g'
    else:
        ia_es_gato = None

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
            if (ia_es_gato and turnos % 2 == 0) or (not ia_es_gato and turnos % 2 == 1):
                print("🤖 Turno de la IA...")
                _, movimiento = minimax(gato, raton, queso, profundidad, turnos % 2 == 0, filas, columnas, obstaculos)
                if turnos % 2 == 0:
                    gato = movimiento
                else:
                    raton = movimiento
            else:
                jugador = "Gato" if turnos % 2 == 0 else "Ratón"
                print(f"🎮 Turno del jugador humano ({jugador})")
                mov = input("Movimiento (WASD + QEZC): ").lower()
                if turnos % 2 == 0:
                    gato = mover_jugador(gato, mov, filas, columnas, obstaculos)
                else:
                    raton = mover_jugador(raton, mov, filas, columnas, obstaculos)
        else:
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
