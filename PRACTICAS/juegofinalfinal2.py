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
    # Distancia Manhattan
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def evaluar_estado(gato, raton, queso):
    if gato == raton:
        return -1000  # Gato atrapó al ratón (pérdida para el ratón)
    if raton == queso:
        return 1000   # Ratón llegó al queso (victoria para ratón)

    dist_gato_raton = distancia(gato, raton)
    dist_raton_queso = distancia(raton, queso)

    # Evaluación que prioriza:
    # Gato quiere estar cerca del ratón (menos distancia)
    # Ratón quiere estar cerca del queso y lejos del gato
    valor = (10 - dist_gato_raton) * 20 + (10 - dist_raton_queso) * 10
    return valor

def minimax(gato, raton, queso, profundidad, max_turno, filas, columnas, obstaculos, alfa=float('-inf'), beta=float('inf')):
    if gato == raton:
        return (-1000, None)
    if raton == queso:
        return (1000, None)
    if profundidad == 0:
        return (evaluar_estado(gato, raton, queso), None)

    if max_turno:  # Turno del gato (maximizar)
        mejor_valor = float('-inf')
        mejor_movimiento = None
        jugador_actual = gato

        for df, dc in DIRECCIONES.values():
            nueva_pos = (jugador_actual[0] + df, jugador_actual[1] + dc)
            if not es_valido(nueva_pos, filas, columnas, obstaculos):
                continue
            nuevo_gato = nueva_pos
            valor, _ = minimax(nuevo_gato, raton, queso, profundidad - 1, False, filas, columnas, obstaculos, alfa, beta)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = nueva_pos
            alfa = max(alfa, mejor_valor)
            if beta <= alfa:
                break
        return (mejor_valor, mejor_movimiento)
    else:  # Turno del ratón (minimizar)
        mejor_valor = float('inf')
        mejor_movimiento = None
        jugador_actual = raton

        for df, dc in DIRECCIONES.values():
            nueva_pos = (jugador_actual[0] + df, jugador_actual[1] + dc)
            if not es_valido(nueva_pos, filas, columnas, obstaculos):
                continue
            nuevo_raton = nueva_pos
            valor, _ = minimax(gato, nuevo_raton, queso, profundidad - 1, True, filas, columnas, obstaculos, alfa, beta)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = nueva_pos
            beta = min(beta, mejor_valor)
            if beta <= alfa:
                break
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
    tablero = crear_tablero(filas, columnas)
    obstaculos = generar_obstaculos(filas, columnas, gato, raton, queso, cantidad=max(5, (filas * columnas) // 10))
    profundidad = 5  # profundidad para IA

    gato_es_ia = False
    raton_es_ia = False

    if modo == 'c':
        tipo_ia = input("¿Quién controlará la IA? (gato=g, ratón=r, ninguno=n): ").lower()
        if tipo_ia == 'g':
            gato_es_ia = True
        elif tipo_ia == 'r':
            raton_es_ia = True
        elif tipo_ia == 'n':
            print("¡Sin IA seleccionada, ambos jugadores serán humanos!")
        else:
            print("Opción inválida, asumiendo sin IA.")
    elif modo == 'j':
        print("Modo jugador contra jugador.")

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

        turno_gato = (turnos % 2 == 0)

        if turno_gato:
            jugador = "Gato"
            es_ia = gato_es_ia
            pos_actual = gato
        else:
            jugador = "Ratón"
            es_ia = raton_es_ia
            pos_actual = raton

        if es_ia:
            print(f"🤖 Turno IA ({jugador})...")
            max_turno = turno_gato
            _, movimiento = minimax(gato, raton, queso, profundidad, max_turno, filas, columnas, obstaculos)
            if movimiento is not None:
                if turno_gato:
                    gato = movimiento
                else:
                    raton = movimiento
        else:
            print(f"🎮 Turno jugador ({jugador})")
            mov = input("Movimiento (w,s,a,d,q,e,z,c): ").lower()
            nueva_pos = mover_jugador(pos_actual, mov, filas, columnas, obstaculos)
            if nueva_pos == pos_actual:
                print("Movimiento inválido o bloqueado.")
            else:
                if turno_gato:
                    gato = nueva_pos
                else:
                    raton = nueva_pos

        turnos += 1

if __name__ == "__main__":
    juego()


