#Juego Gato vs Raton 

import sys

# Definición de símbolos visuales para el juego
gato = "🐱"
raton = "🐭"
vacio = "⬜"
obstaculo = "🟥"

# Número máximo de turnos antes de que termine el juego
limite_turnos = 20

# Diccionario que mapea teclas a movimientos (solo 4 direcciones)
movimientos_permitidos = {
    'w': (-1, 0),   # Mover hacia arriba (disminuye fila)
    's': (1, 0),    # Mover hacia abajo (aumenta fila)
    'a': (0, -1),   # Mover hacia izquierda (disminuye columna)
    'd': (0, 1),    # Mover hacia derecha (aumenta columna)
}

def crear_tablero_vacio(numero_filas, numero_columnas):
    """
    Crea un tablero vacío lleno de celdas vacías
    Parámetros:
        numero_filas: cantidad de filas del tablero
        numero_columnas: cantidad de columnas del tablero
    Retorna: matriz bidimensional representando el tablero
    """
    return [[vacio for _ in range(numero_columnas)] for _ in range(numero_filas)]

def mostrar_tablero(tablero_juego):
    """
    Imprime el tablero en la consola de manera visual
    Parámetros:
        tablero_juego: matriz que representa el estado actual del tablero
    """
    for fila_actual in tablero_juego:
        print(" ".join(fila_actual))  # Une los elementos de cada fila con espacios
    print()  # Línea en blanco para separar turnos

def es_posicion_valida(posicion_a_verificar, total_filas, total_columnas):
    """
    Verifica si una posición está dentro de los límites del tablero
    Parámetros:
        posicion_a_verificar: tupla (fila, columna) a verificar
        total_filas: número total de filas del tablero
        total_columnas: número total de columnas del tablero
    Retorna: True si la posición es válida, False en caso contrario
    """
    fila, columna = posicion_a_verificar
    return 0 <= fila < total_filas and 0 <= columna < total_columnas

def calcular_nueva_posicion(posicion_actual, tecla_presionada, total_filas, total_columnas):
    """
    Calcula la nueva posición después de un movimiento
    Parámetros:
        posicion_actual: tupla (fila, columna) de la posición actual
        tecla_presionada: tecla que indica la dirección del movimiento
        total_filas: número total de filas del tablero
        total_columnas: número total de columnas del tablero
    Retorna: nueva posición si es válida, posición actual si no es válida
    """
    # Obtiene el cambio en fila y columna según la tecla presionada
    cambio_fila, cambio_columna = movimientos_permitidos.get(tecla_presionada, (0, 0))
    
    # Calcula la nueva posición sumando los cambios
    nueva_posicion = (posicion_actual[0] + cambio_fila, posicion_actual[1] + cambio_columna)
    
    # Retorna la nueva posición si es válida, sino mantiene la posición actual
    return nueva_posicion if es_posicion_valida(nueva_posicion, total_filas, total_columnas) else posicion_actual

def obtener_movimientos_posibles(posicion_personaje, tablero_juego):
    """
    Obtiene todas las posiciones válidas a las que se puede mover un personaje
    Parámetros:
        posicion_personaje: tupla (fila, columna) de la posición actual del personaje
        tablero_juego: matriz que representa el estado actual del tablero
    Retorna: lista de tuplas con todas las posiciones válidas de movimiento
    """
    total_filas, total_columnas = len(tablero_juego), len(tablero_juego[0])
    movimientos_validos = []
    
    # Recorre todas las direcciones posibles
    for cambio_fila, cambio_columna in movimientos_permitidos.values():
        nueva_posicion = (posicion_personaje[0] + cambio_fila, posicion_personaje[1] + cambio_columna)
        
        # Verifica si la nueva posición es válida y no es un obstáculo
        if (es_posicion_valida(nueva_posicion, total_filas, total_columnas) and 
            tablero_juego[nueva_posicion[0]][nueva_posicion[1]] != obstaculo):
            movimientos_validos.append(nueva_posicion)
    
    return movimientos_validos

def evaluar_situacion_juego(posicion_raton, posicion_gato, numero_turno, limite_turnos):
    """
    Evalúa qué tan buena o mala es la situación actual del juego desde la perspectiva del ratón
    Parámetros:
        posicion_raton: tupla (fila, columna) de la posición del ratón
        posicion_gato: tupla (fila, columna) de la posición del gato
        numero_turno: turno actual del juego
        limite_turnos: número máximo de turnos permitidos
    Retorna: puntuación numérica (positiva=buena para ratón, negativa=buena para gato)
    """
    # Si el gato atrapó al ratón (misma posición), el ratón pierde
    if posicion_raton == posicion_gato:
        return -100
    
    # Si se alcanzó el límite de turnos, el ratón sobrevivió y gana
    if numero_turno >= limite_turnos:
        return 50
    
    # Calcula distancia Manhattan entre gato y ratón (mientras más lejos, mejor para el ratón)
    distancia_manhattan = abs(posicion_raton[0] - posicion_gato[0]) + abs(posicion_raton[1] - posicion_gato[1])
    return -distancia_manhattan  # Negativo porque queremos maximizar la distancia

def algoritmo_minimax(tablero_juego, posicion_raton, posicion_gato, numero_turno, limite_turnos, profundidad_busqueda, es_turno_raton):
    """
    Algoritmo minimax para determinar el mejor movimiento
    Parámetros:
        tablero_juego: matriz que representa el estado actual del tablero
        posicion_raton: tupla (fila, columna) de la posición del ratón
        posicion_gato: tupla (fila, columna) de la posición del gato
        numero_turno: turno actual del juego
        limite_turnos: número máximo de turnos permitidos
        profundidad_busqueda: qué tan profundo buscar en el árbol de posibilidades
        es_turno_raton: True si es turno del ratón, False si es turno del gato
    Retorna: tupla (puntuación, mejor_movimiento)
    """
    # Condiciones de parada: profundidad 0, juego terminado
    if (profundidad_busqueda == 0 or posicion_raton == posicion_gato or numero_turno >= limite_turnos):
        return evaluar_situacion_juego(posicion_raton, posicion_gato, numero_turno, limite_turnos), None

    if es_turno_raton:
        # Turno del ratón: busca maximizar la puntuación
        mejor_puntuacion = -float('inf')  # Inicializa con el peor valor posible
        mejor_movimiento = None
        
        # Evalúa todos los movimientos posibles del ratón
        for movimiento_posible in obtener_movimientos_posibles(posicion_raton, tablero_juego):
            puntuacion_movimiento, _ = algoritmo_minimax(
                tablero_juego, movimiento_posible, posicion_gato, 
                numero_turno + 1, limite_turnos, profundidad_busqueda - 1, False
            )
            
            # Si encuentra un movimiento mejor, lo guarda
            if puntuacion_movimiento > mejor_puntuacion:
                mejor_puntuacion = puntuacion_movimiento
                mejor_movimiento = movimiento_posible
        
        return mejor_puntuacion, mejor_movimiento
    else:
        # Turno del gato: busca minimizar la puntuación (malo para el ratón)
        peor_puntuacion = float('inf')  # Inicializa con el mejor valor posible para el ratón
        mejor_movimiento_gato = None
        
        # Evalúa todos los movimientos posibles del gato
        for movimiento_posible in obtener_movimientos_posibles(posicion_gato, tablero_juego):
            puntuacion_movimiento, _ = algoritmo_minimax(
                tablero_juego, posicion_raton, movimiento_posible, 
                numero_turno + 1, limite_turnos, profundidad_busqueda - 1, True
            )
            
            # Si encuentra un movimiento que sea peor para el ratón, lo guarda
            if puntuacion_movimiento < peor_puntuacion:
                peor_puntuacion = puntuacion_movimiento
                mejor_movimiento_gato = movimiento_posible
        
        return peor_puntuacion, mejor_movimiento_gato

def iniciar_juego():
    """
    Función principal que maneja todo el flujo del juego
    """
    # Configuración inicial del juego
    modo_juego = input("¿Querés jugar contra la Computadora (c) o contra otro Jugador (j)? ").lower()
    numero_filas = int(input("¿Cuántas filas querés que tenga el tablero? (mínimo 5): "))
    numero_columnas = int(input("¿Cuántas columnas querés que tenga el tablero? (mínimo 5): "))

    # Creación del tablero y posicionamiento inicial
    tablero_principal = crear_tablero_vacio(numero_filas, numero_columnas)
    posicion_gato = (0, 0)  # Gato empieza en esquina superior izquierda
    posicion_raton = (numero_filas - 1, numero_columnas - 1)  # Ratón en esquina inferior derecha

    # Coloca los personajes en el tablero
    tablero_principal[posicion_gato[0]][posicion_gato[1]] = gato
    tablero_principal[posicion_raton[0]][posicion_raton[1]] = raton

    # Coloca obstáculos verticales fijos en el tablero
    for indice_fila in range(1, numero_filas - 1):
        tablero_principal[indice_fila][numero_columnas // 3] = obstaculo
        tablero_principal[indice_fila][2 * numero_columnas // 3] = obstaculo

    # Inicializa el contador de turnos
    contador_turnos = 0

    # Configuración de jugadores según el modo de juego
    if modo_juego == 'c':
        # Modo contra computadora
        eleccion_jugador = input("¿Querés ser el Gato (g) o el Ratón (r)? ").lower()
        controlador_gato = "jugador" if eleccion_jugador == 'g' else "ia"
        controlador_raton = "jugador" if eleccion_jugador == 'r' else "ia"
    else:
        # Modo jugador vs jugador
        eleccion_jugador1 = input("Jugador 1, ¿querés ser el Gato (g) o el Ratón (r)? ").lower()
        if eleccion_jugador1 == 'g':
            controlador_gato = "jugador1"
            controlador_raton = "jugador2"
        else:
            controlador_gato = "jugador2"
            controlador_raton = "jugador1"

    # Bucle principal del juego
    while True:
        mostrar_tablero(tablero_principal)  # Muestra el estado actual del tablero

        # Determina de quién es el turno (turnos pares=ratón, impares=gato)
        quien_juega = controlador_raton if contador_turnos % 2 == 0 else controlador_gato
        es_turno_del_raton = contador_turnos % 2 == 0

        # Obtiene la posición actual del personaje que debe moverse
        posicion_actual = posicion_raton if es_turno_del_raton else posicion_gato

        # Procesa el movimiento según quién controla el personaje
        if quien_juega.startswith("jugador"):
            # Movimiento controlado por jugador humano
            nombre_personaje = 'Ratón 🐭' if es_turno_del_raton else 'Gato 🐱'
            print(f"Turno de {quien_juega} ({nombre_personaje})")
            tecla_movimiento = input("Movimiento (w=arriba/s=abajo/a=izquierda/d=derecha): ").lower()
            nueva_posicion = calcular_nueva_posicion(posicion_actual, tecla_movimiento, numero_filas, numero_columnas)
        else:
            # Movimiento controlado por IA
            nombre_personaje = 'Ratón 🐭' if es_turno_del_raton else 'Gato 🐱'
            print(f"Turno de la IA ({nombre_personaje})")
            # Usa minimax con profundidad 4 para calcular el mejor movimiento
            _, nueva_posicion = algoritmo_minimax(
                tablero_principal, posicion_raton, posicion_gato, 
                contador_turnos, limite_turnos, 4, es_turno_del_raton
            )

        # Actualiza la posición del personaje en el tablero
        if es_turno_del_raton:
            # Verifica si el ratón intenta moverse a un obstáculo
            if tablero_principal[nueva_posicion[0]][nueva_posicion[1]] == obstaculo:
                nueva_posicion = posicion_raton  # Mantiene la posición actual
            
            # Actualiza la posición del ratón en el tablero
            tablero_principal[posicion_raton[0]][posicion_raton[1]] = vacio
            posicion_raton = nueva_posicion
            tablero_principal[posicion_raton[0]][posicion_raton[1]] = raton
        else:
            # Verifica si el gato intenta moverse a un obstáculo
            if tablero_principal[nueva_posicion[0]][nueva_posicion[1]] == obstaculo:
                nueva_posicion = posicion_gato  # Mantiene la posición actual
            
            # Actualiza la posición del gato en el tablero
            tablero_principal[posicion_gato[0]][posicion_gato[1]] = vacio
            posicion_gato = nueva_posicion
            tablero_principal[posicion_gato[0]][posicion_gato[1]] = gato

        # Incrementa el contador de turnos
        contador_turnos += 1

        # Verifica las condiciones de fin de juego
        if posicion_raton == posicion_gato:
            # El gato atrapó al ratón
            mostrar_tablero(tablero_principal)
            print("¡El gato atrapó al ratón! 🐱🐭")
            break
        
        if contador_turnos >= limite_turnos:
            # Se alcanzó el límite de turnos, el ratón sobrevivió
            mostrar_tablero(tablero_principal)
            print("¡El ratón sobrevivió todos los turnos! 🐭🎉")
            break

# Inicia el juego
iniciar_juego()
