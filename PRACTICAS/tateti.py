#TA TE TI 
import math

# Inicializar el tablero
def crear_tablero():
    return [' ' for _ in range(9)]

# Mostrar el tablero
def mostrar_tablero(tablero):
    for fila in [tablero[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(fila) + ' |')

# Verificar si hay ganador
def hay_ganador(tablero, jugador):
    combinaciones = [
        [0,1,2], [3,4,5], [6,7,8],  # filas
        [0,3,6], [1,4,7], [2,5,8],  # columnas
        [0,4,8], [2,4,6]            # diagonales
    ]
    return any(all(tablero[i] == jugador for i in combo) for combo in combinaciones)

# Verificar si hay empate
def empate(tablero):
    return ' ' not in tablero

# Obtener los movimientos posibles
def movimientos_disponibles(tablero):
    return [i for i, x in enumerate(tablero) if x == ' ']

# Minimax
def minimax(tablero, profundidad, es_maximizador):
    if hay_ganador(tablero, 'O'):
        return 1
    elif hay_ganador(tablero, 'X'):
        return -1
    elif empate(tablero):
        return 0

    if es_maximizador:
        mejor_puntaje = -math.inf
        for movimiento in movimientos_disponibles(tablero):
            tablero[movimiento] = 'O'
            puntaje = minimax(tablero, profundidad + 1, False)
            tablero[movimiento] = ' '
            mejor_puntaje = max(mejor_puntaje, puntaje)
        return mejor_puntaje
    else:
        mejor_puntaje = math.inf
        for movimiento in movimientos_disponibles(tablero):
            tablero[movimiento] = 'X'
            puntaje = minimax(tablero, profundidad + 1, True)
            tablero[movimiento] = ' '
            mejor_puntaje = min(mejor_puntaje, puntaje)
        return mejor_puntaje

# Movimiento de la IA
def movimiento_ia(tablero):
    mejor_puntaje = -math.inf
    mejor_movimiento = None
    for movimiento in movimientos_disponibles(tablero):
        tablero[movimiento] = 'O'
        puntaje = minimax(tablero, 0, False)
        tablero[movimiento] = ' '
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = movimiento
    tablero[mejor_movimiento] = 'O'

# Juego principal
def jugar():
    tablero = crear_tablero()
    jugador = input("¿Quieres ser X o O? (Tú juegas primero): ").upper()
    ia = 'O' if jugador == 'X' else 'X'

    turno_jugador = True if jugador == 'X' else False

    while True:
        mostrar_tablero(tablero)
        if hay_ganador(tablero, jugador):
            print("¡Ganaste!")
            break
        elif hay_ganador(tablero, ia):
            print("¡La IA ganó!")
            break
        elif empate(tablero):
            print("¡Empate!")
            break

        if turno_jugador:
            try:
                movimiento = int(input("Elige una posición (0-8): "))
                if tablero[movimiento] == ' ':
                    tablero[movimiento] = jugador
                    turno_jugador = False
                else:
                    print("¡Posición ocupada!")
            except:
                print("Entrada inválida.")
        else:
            print("Turno de la IA...")
            movimiento_ia(tablero)
            turno_jugador = True

# Ejecutar juego
if __name__ == "__main__":
    jugar()
