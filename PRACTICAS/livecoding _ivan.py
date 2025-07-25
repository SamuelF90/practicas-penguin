tamano = 5
tablero = [['.' for _ in range (tamano)] for _ in range (tamano) ]
fila_gato , columna_gato = 0,0
tablero [0][0] = 'g'
fila_raton , columna_raton = 4,4
tablero [-1][-1] = 'r'

for fila in tablero:
    print(" ".join(fila))
 


