class MapaJuego:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [['.' for _ in range(columnas)] for _ in range(filas)]

    def mostrar_matriz(self):
        for fila in self.mapa:
            print(" ".join(fila))
        print()  # Salto de línea extra para claridad

    def colocar_entrada_salida(self, entrada, salida):
        self.mapa[entrada[0]][entrada[1]] = 'E'
        self.mapa[salida[0]][salida[1]] = 'S'

    def colocar_obstaculo(self, obstaculo):
        self.mapa[obstaculo[0]][obstaculo[1]] = 'X'


def main():
    filas = int(input("Ingrese filas: "))
    columnas = int(input("Ingrese columnas: "))

    juego = MapaJuego(filas, columnas)
    juego.mostrar_matriz()

    entrada_fila = int(input("Ingrese entrada fila: "))
    entrada_col = int(input("Ingrese entrada columna: "))
    salida_fila = int(input("Ingrese salida fila: "))
    salida_col = int(input("Ingrese salida columna: "))

    entrada = (entrada_fila, entrada_col)
    salida = (salida_fila, salida_col)
    juego.colocar_entrada_salida(entrada, salida)
    juego.mostrar_matriz()

    obs_fila = int(input("Ingrese la fila del obstáculo: "))
    obs_col = int(input("Ingrese la columna del obstáculo: "))
    obstaculo = (obs_fila, obs_col)
    juego.colocar_obstaculo(obstaculo)
    juego.mostrar_matriz()


if __name__ == "__main__":
    main()
