
# GAME CAT VS RAT

def juego():
    filas = int(input("Indique el tamaño de filas del tablero (5 o 10): "))
    columnas = int(input("Indique el tamaño de columnas del tablero (5 o 10): "))

    # Validación estricta del tamaño del tablero
    if not ((filas == 5 and columnas == 5) or (filas == 10 and columnas == 10)):
        print("❌ Solo se permiten tableros de 5x5 o 10x10.")
        return

    modo = input("¿Quieres jugar contra la computadora o contra un jugador? (c/j): ").lower()

    tablero = crear_tablero(filas, columnas)

    # Ratón en (0, 0)
    raton = (0, 0)

    # Gato en (4,4) si 5x5, en (9,9) si 10x10
    gato = (4, 4) if filas == 5 else (9, 9)

    # Queso en la esquina inferior derecha
    queso = (filas - 1, columnas - 1)

    obstaculos = generar_obstaculos(
        filas, columnas, gato, raton, queso,
        cantidad=max(5, (filas * columnas) // 10)
    )

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
                if movimiento is not None:
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


