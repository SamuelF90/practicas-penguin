
import sys

EMOJI_GATO = "🐱"
EMOJI_RATON = "🐭"
EMOJI_QUESO = "🧀"
EMOJI_VACIO = "⬜"
EMOJI_OBSTACULO = "🟥"

MAX_TURNOS = 20

DIRECCIONES = {
    'w': (-1, 0),   # Arriba
    's': (1, 0),    # Abajo
    'a': (0, -1),   # Izquierda
    'd': (0, 1),    # Derecha
    'q': (-1, -1),  # Arriba izquierda
    'e': (-1, 1),   # Arriba derecha
    'z': (1, -1),   # Abajo izquierda
    'c': (1, 1),    # Abajo derecha
}

def crear_tablero(filas, columnas):
    return [[EMOJI_VACIO for _ in range(columnas)] for _ in range(filas)]

def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
    print()

def posicion_valida(pos, filas, columnas):
    x, y = pos
    return 0 <= x < filas and 0 <= y < columnas

def mover(pos, direccion, filas, columnas):
    dx, dy = DIRECCIONES.get(direccion, (0, 0))
    nueva = (pos[0] + dx, pos[1] + dy)
    return nueva if posicion_valida(nueva, filas, columnas) else pos

def obtener_movimientos(pos, tablero):
    filas, columnas = len(tablero), len(tablero[0])
    movimientos = []
    for dx, dy in DIRECCIONES.values():
        nueva = (pos[0] + dx, pos[1] + dy)
        if posicion_valida(nueva, filas, columnas) and tablero[nueva[0]][nueva[1]] != EMOJI_OBSTACULO:
            movimientos.append(nueva)
    return movimientos

def evaluar_estado(raton, gato, queso, turno, max_turnos):
    if raton == gato:
        return -100  # el ratón pierde
    if raton == queso:
        return 100  # el ratón gana
    if turno >= max_turnos:
        return 50  # el ratón sobrevive
    return -abs(raton[0] - gato[0]) - abs(raton[1] - gato[1])

def minimax(tablero, raton, gato, queso, turno, max_turnos, profundidad, max_jugador):
    if profundidad == 0 or raton == gato or raton == queso or turno >= max_turnos:
        return evaluar_estado(raton, gato, queso, turno, max_turnos), None

    if max_jugador:
        mejor_valor = -float('inf')
        mejor_mov = None
        for mov in obtener_movimientos(raton, tablero):
            valor, _ = minimax(tablero, mov, gato, queso, turno + 1, max_turnos, profundidad - 1, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        return mejor_valor, mejor_mov
    else:
        peor_valor = float('inf')
        peor_mov = None
        for mov in obtener_movimientos(gato, tablero):
            valor, _ = minimax(tablero, raton, mov, queso, turno + 1, max_turnos, profundidad - 1, True)
            if valor < peor_valor:
                peor_valor = valor
                peor_mov = mov
        return peor_valor, peor_mov

def jugar():
    modo = input("¿Querés jugar contra la Computadora (c) o contra otro Jugador (j)? ").lower()
    filas = int(input("¿Cuántas filas querés que tenga el tablero? (mínimo 5): "))
    columnas = int(input("¿Cuántas columnas querés que tenga el tablero? (mínimo 5): "))

    tablero = crear_tablero(filas, columnas)
    gato = (0, 0)
    raton = (filas - 1, columnas - 1)
    queso = (filas // 2, columnas // 2)

    tablero[gato[0]][gato[1]] = EMOJI_GATO
    tablero[raton[0]][raton[1]] = EMOJI_RATON
    tablero[queso[0]][queso[1]] = EMOJI_QUESO

    # Obstáculos fijos
    for i in range(1, filas - 1):
        tablero[i][columnas // 3] = EMOJI_OBSTACULO
        tablero[i][2 * columnas // 3] = EMOJI_OBSTACULO

    turno = 0

    if modo == 'c':
        eleccion = input("¿Querés ser el Gato (g) o el Ratón (r)? ").lower()
        jugador_gato = "jugador" if eleccion == 'g' else "ia"
        jugador_raton = "jugador" if eleccion == 'r' else "ia"
    else:
        eleccion_j1 = input("Jugador 1, ¿querés ser el Gato (g) o el Ratón (r)? ").lower()
        if eleccion_j1 == 'g':
            jugador_gato = "jugador1"
            jugador_raton = "jugador2"
        else:
            jugador_gato = "jugador2"
            jugador_raton = "jugador1"

    while True:
        imprimir_tablero(tablero)

        jugador_turno = jugador_raton if turno % 2 == 0 else jugador_gato
        es_raton = turno % 2 == 0

        pos_actual = raton if es_raton else gato

        if jugador_turno.startswith("jugador"):
            print(f"Turno de {jugador_turno} ({'Ratón 🐭' if es_raton else 'Gato 🐱'})")
            tecla = input("Movimiento (w/a/s/d/q/e/z/c): ").lower()
            nueva_pos = mover(pos_actual, tecla, filas, columnas)
        else:
            print(f"Turno de la IA ({'Ratón 🐭' if es_raton else 'Gato 🐱'})")
            _, nueva_pos = minimax(tablero, raton, gato, queso, turno, MAX_TURNOS, 4, es_raton)

        if es_raton:
            if tablero[nueva_pos[0]][nueva_pos[1]] == EMOJI_OBSTACULO:
                nueva_pos = raton
            tablero[raton[0]][raton[1]] = EMOJI_VACIO
            raton = nueva_pos
            tablero[raton[0]][raton[1]] = EMOJI_RATON
        else:
            if tablero[nueva_pos[0]][nueva_pos[1]] == EMOJI_OBSTACULO:
                nueva_pos = gato
            tablero[gato[0]][gato[1]] = EMOJI_VACIO
            gato = nueva_pos
            tablero[gato[0]][gato[1]] = EMOJI_GATO

        turno += 1

        if raton == gato:
            imprimir_tablero(tablero)
            print("¡El gato atrapó al ratón! 🐱🐭")
            break
        if raton == queso:
            imprimir_tablero(tablero)
            print("¡El ratón llegó al queso! 🧀🐭")
            break
        if turno >= MAX_TURNOS:
            imprimir_tablero(tablero)
            print("¡El ratón sobrevivió los turnos! 🐭🎉")
            break

jugar()



