
# Constantes para el tablero
ANCHO = 10
ALTO = 10
MAX_TURNOS = 20

# Símbolos del tablero
VACIO = '⬜'
GATO = '🐱'
RATON = '🐭'
QUESO = '🧀'
OBSTACULO = '🟥'

# Movimientos posibles (8 direcciones)
MOVIMIENTOS = {
    'w': (-1, 0),   # arriba
    's': (1, 0),    # abajo
    'a': (0, -1),   # izquierda
    'd': (0, 1),    # derecha
    'q': (-1, -1),  # diagonal arriba-izquierda
    'e': (-1, 1),   # diagonal arriba-derecha
    'z': (1, -1),   # diagonal abajo-izquierda
    'c': (1, 1)     # diagonal abajo-derecha
}

def crear_tablero():
    tablero = [[VACIO for _ in range(ANCHO)] for _ in range(ALTO)]
    obstaculos_fijos = [(2, 2), (3, 3), (1, 5), (4, 1)]
    for (f, c) in obstaculos_fijos:
        if 0 <= f < ALTO and 0 <= c < ANCHO:
            tablero[f][c] = OBSTACULO
    return tablero

def imprimir_tablero(tablero, gato, raton, queso):
    for f in range(ALTO):
        fila = ''
        for c in range(ANCHO):
            if (f, c) == gato:
                fila += GATO
            elif (f, c) == raton:
                fila += RATON
            elif (f, c) == queso:
                fila += QUESO
            else:
                fila += tablero[f][c]
        print(fila)
    print()

def es_valida(pos, tablero):
    f, c = pos
    if 0 <= f < ALTO and 0 <= c < ANCHO:
        if tablero[f][c] != OBSTACULO:
            return True
    return False

def movimientos_validos(pos, tablero):
    movs = []
    for df, dc in MOVIMIENTOS.values():
        nueva = (pos[0] + df, pos[1] + dc)
        if es_valida(nueva, tablero):
            movs.append(nueva)
    return movs

def es_fin_juego(gato, raton, queso, turnos):
    if gato == raton:
        return True, 'Gato atrapó al ratón. ¡Gana el gato!'
    if raton == queso:
        return True, 'Ratón llegó al queso. ¡Gana el ratón!'
    if turnos >= MAX_TURNOS:
        return True, 'Máximo de turnos alcanzado. ¡Gana el ratón por supervivencia!'
    return False, ''

def minimax(gato, raton, queso, tablero, turnos, es_turno_gato, profundidad=3):
    fin, mensaje = es_fin_juego(gato, raton, queso, turnos)
    if fin or profundidad == 0:
        if gato == raton:
            return 1000
        elif raton == queso or turnos >= MAX_TURNOS:
            return -1000
        else:
            dist_gato_raton = abs(gato[0]-raton[0]) + abs(gato[1]-raton[1])
            dist_raton_queso = abs(raton[0]-queso[0]) + abs(raton[1]-queso[1])
            return dist_gato_raton - dist_raton_queso

    if es_turno_gato:
        mejor_valor = -float('inf')
        for mov in movimientos_validos(gato, tablero):
            valor = minimax(mov, raton, queso, tablero, turnos+1, False, profundidad-1)
            if valor > mejor_valor:
                mejor_valor = valor
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for mov in movimientos_validos(raton, tablero):
            valor = minimax(gato, mov, queso, tablero, turnos+1, True, profundidad-1)
            if valor < mejor_valor:
                mejor_valor = valor
        return mejor_valor

def mejor_movimiento(pos_actual, tablero, queso, turno_gato, gato, raton):
    mejor_valor = -float('inf') if turno_gato else float('inf')
    mejor_mov = pos_actual
    for mov in movimientos_validos(pos_actual, tablero):
        if turno_gato:
            valor = minimax(mov, raton, queso, tablero, 0, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        else:
            valor = minimax(gato, mov, queso, tablero, 0, True)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
    return mejor_mov

def mover(pos, tecla, tablero):
    if tecla not in MOVIMIENTOS:
        return pos
    df, dc = MOVIMIENTOS[tecla]
    nueva = (pos[0]+df, pos[1]+dc)
    if es_valida(nueva, tablero):
        return nueva
    return pos

def jugar():
    tablero = crear_tablero()

    gato = (0, 0)
    raton = (ALTO-1, ANCHO-1)
    queso = (ALTO//2, ANCHO-1)

    jugador = ''
    while jugador not in ['g', 'r']:
        jugador = input("¿Querés ser Gato (g) o Ratón (r)? ").lower()

    turno = 0
    turno_jugador_gato = (jugador == 'g')

    while True:
        imprimir_tablero(tablero, gato, raton, queso)
        fin, mensaje = es_fin_juego(gato, raton, queso, turno)
        if fin:
            print(mensaje)
            break

        if turno_jugador_gato:
            print("Turno jugador Gato")
            tecla = input("Mover (w/a/s/d/q/e/z/c): ").lower()
            gato = mover(gato, tecla, tablero)
            raton = mejor_movimiento(raton, tablero, queso, False, gato, raton)
        else:
            print("Turno jugador Ratón")
            tecla = input("Mover (w/a/s/d/q/e/z/c): ").lower()
            raton = mover(raton, tecla, tablero)
            gato = mejor_movimiento(gato, tablero, queso, True, gato, raton)

        turno += 1

if __name__ == "__main__":
    jugar()


