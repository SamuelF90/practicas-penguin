
import sys

gato = "🐱"
raton = "🐭"
vacio = "⬜"
obstaculo = "🟥"

limite_turnos = 20

movimientos_permitidos = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1),
}

def crear_tablero_vacio(numero_filas, numero_columnas):
    return [[vacio for _ in range(numero_columnas)] for _ in range(numero_filas)]

def mostrar_tablero(tablero_juego):
    for fila_actual in tablero_juego:
        print(" ".join(fila_actual))
    print()

def es_posicion_valida(posicion_a_verificar, total_filas, total_columnas):
    fila, columna = posicion_a_verificar
    return 0 <= fila < total_filas and 0 <= columna < total_columnas

def calcular_nueva_posicion(posicion_actual, tecla_presionada, total_filas, total_columnas):
    cambio_fila, cambio_columna = movimientos_permitidos.get(tecla_presionada, (0, 0))
    nueva_posicion = (posicion_actual[0] + cambio_fila, posicion_actual[1] + cambio_columna)
    return nueva_posicion if es_posicion_valida(nueva_posicion, total_filas, total_columnas) else posicion_actual

def obtener_movimientos_posibles(posicion_personaje, tablero_juego):
    total_filas, total_columnas = len(tablero_juego), len(tablero_juego[0])
    movimientos_validos = []
    
    for cambio_fila, cambio_columna in movimientos_permitidos.values():
        nueva_posicion = (posicion_personaje[0] + cambio_fila, posicion_personaje[1] + cambio_columna)
        
        if (es_posicion_valida(nueva_posicion, total_filas, total_columnas) and 
            tablero_juego[nueva_posicion[0]][nueva_posicion[1]] != obstaculo):
            movimientos_validos.append(nueva_posicion)
    
    return movimientos_validos

def evaluar_situacion_juego(posicion_raton, posicion_gato, numero_turno, limite_turnos):
    if posicion_raton == posicion_gato:
        return -100
    
    if numero_turno >= limite_turnos:
        return 50
    
    distancia_manhattan = abs(posicion_raton[0] - posicion_gato[0]) + abs(posicion_raton[1] - posicion_gato[1])
    return -distancia_manhattan

def algoritmo_minimax(tablero_juego, posicion_raton, posicion_gato, numero_turno, limite_turnos, profundidad_busqueda, es_turno_raton):
    if (profundidad_busqueda == 0 or posicion_raton == posicion_gato or numero_turno >= limite_turnos):
        return evaluar_situacion_juego(posicion_raton, posicion_gato, numero_turno, limite_turnos), None

    if es_turno_raton:
        mejor_puntuacion = -float('inf')
        mejor_movimiento = None
        
        for movimiento_posible in obtener_movimientos_posibles(posicion_raton, tablero_juego):
            puntuacion_movimiento, _ = algoritmo_minimax(
                tablero_juego, movimiento_posible, posicion_gato, 
                numero_turno + 1, limite_turnos, profundidad_busqueda - 1, False
            )
            
            if puntuacion_movimiento > mejor_puntuacion:
                mejor_puntuacion = puntuacion_movimiento
                mejor_movimiento = movimiento_posible
        
        return mejor_puntuacion, mejor_movimiento
    else:
        peor_puntuacion = float('inf')
        mejor_movimiento_gato = None
        
        for movimiento_posible in obtener_movimientos_posibles(posicion_gato, tablero_juego):
            puntuacion_movimiento, _ = algoritmo_minimax(
                tablero_juego, posicion_raton, movimiento_posible, 
                numero_turno + 1, limite_turnos, profundidad_busqueda - 1, True
            )
            
            if puntuacion_movimiento < peor_puntuacion:
                peor_puntuacion = puntuacion_movimiento
                mejor_movimiento_gato = movimiento_posible
        
        return peor_puntuacion, mejor_movimiento_gato

def iniciar_juego():
    modo_juego = input("¿Querés jugar contra la Computadora (c) o contra otro Jugador (j)? ").lower()
    numero_filas = int(input("¿Cuántas filas querés que tenga el tablero? (mínimo 5): "))
    numero_columnas = int(input("¿Cuántas columnas querés que tenga el tablero? (mínimo 5): "))

    tablero_principal = crear_tablero_vacio(numero_filas, numero_columnas)
    posicion_gato = (0, 0)
    posicion_raton = (numero_filas - 1, numero_columnas - 1)

    tablero_principal[posicion_gato[0]][posicion_gato[1]] = gato
    tablero_principal[posicion_raton[0]][posicion_raton[1]] = raton

    for indice_fila in range(1, numero_filas - 1):
        tablero_principal[indice_fila][numero_columnas // 3] = obstaculo
        tablero_principal[indice_fila][2 * numero_columnas // 3] = obstaculo

    contador_turnos = 0

    if modo_juego == 'c':
        eleccion_jugador = input("¿Querés ser el Gato (g) o el Ratón (r)? ").lower()
        controlador_gato = "jugador" if eleccion_jugador == 'g' else "ia"
        controlador_raton = "jugador" if eleccion_jugador == 'r' else "ia"
    else:
        eleccion_jugador1 = input("Jugador 1, ¿querés ser el Gato (g) o el Ratón (r)? ").lower()
        if eleccion_jugador1 == 'g':
            controlador_gato = "jugador1"
            controlador_raton = "jugador2"
        else:
            controlador_gato = "jugador2"
            controlador_raton = "jugador1"

    while True:
        mostrar_tablero(tablero_principal)

        quien_juega = controlador_raton if contador_turnos % 2 == 0 else controlador_gato
        es_turno_del_raton = contador_turnos % 2 == 0

        posicion_actual = posicion_raton if es_turno_del_raton else posicion_gato

        if quien_juega.startswith("jugador"):
            nombre_personaje = 'Ratón 🐭' if es_turno_del_raton else 'Gato 🐱'
            print(f"Turno de {quien_juega} ({nombre_personaje})")
            tecla_movimiento = input("Movimiento (w=arriba/s=abajo/a=izquierda/d=derecha): ").lower()
            nueva_posicion = calcular_nueva_posicion(posicion_actual, tecla_movimiento, numero_filas, numero_columnas)
        else:
            nombre_personaje = 'Ratón 🐭' if es_turno_del_raton else 'Gato 🐱'
            print(f"Turno de la IA ({nombre_personaje})")
            _, nueva_posicion = algoritmo_minimax(
                tablero_principal, posicion_raton, posicion_gato, 
                contador_turnos, limite_turnos, 4, es_turno_del_raton
            )

        if es_turno_del_raton:
            if tablero_principal[nueva_posicion[0]][nueva_posicion[1]] == obstaculo:
                nueva_posicion = posicion_raton
            
            tablero_principal[posicion_raton[0]][posicion_raton[1]] = vacio
            posicion_raton = nueva_posicion
            tablero_principal[posicion_raton[0]][posicion_raton[1]] = raton
        else:
            if tablero_principal[nueva_posicion[0]][nueva_posicion[1]] == obstaculo:
                nueva_posicion = posicion_gato
            
            tablero_principal[posicion_gato[0]][posicion_gato[1]] = vacio
            posicion_gato = nueva_posicion
            tablero_principal[posicion_gato[0]][posicion_gato[1]] = gato

        contador_turnos += 1

        if posicion_raton == posicion_gato:
            mostrar_tablero(tablero_principal)
            print("¡El gato atrapó al ratón! 🐱🐭")
            break
        
        if contador_turnos >= limite_turnos:
            mostrar_tablero(tablero_principal)
            print("¡El ratón sobrevivió todos los turnos! 🐭🎉")
            break

iniciar_juego()