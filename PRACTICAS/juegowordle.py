#JUEGO

#Definir palabra a encontrar, intentos,cantidad de letras
palabra_a_encontrar = 'virus'
cantidad_letras = '5'
intentos = '5'
#comparamos las palabras (posicion correcta,si existe en la palabra o si no existe)
def verificar_palabra_ingresada(palabra_a_encontrar,palabra_ingresada):


#definir una lista y agregar las letras verificadas
resultado = []

for posicion in range(cantidad_letras):
    las_letras_son_iguales = palabra_a_encontrar
    [posicion] == palabra_ingresada[posicion]
    la_letra_existe = palabra_ingresada[posicion] in palabra_a_encontrar
    if las_letras_son_iguales:
        resultado.append('[+palabra_ingresada[posicion]+']')
    elif la_letra_existe:
        resultado.append(palabra_ingresada[posicion])
    else:
    
        return resultado
    
    

        

#hacer la grilla
def imprimir grilla(grilla):
cantidad_de_filas = len(grilla)
    for fila in range (cantidad_de_filas)
        print(grilla[])
    

#bienvenida a wordle
print("Bienvenido al Wordle")
#restar la cantidad de intentos
while > 0 :
print(f 'Te quedan {intentos}')
palabra_ingresada = input ("ingrese la palabra")
intentos = intentos - 1
if len(palabra_ingresada) != cantidad_letras:
    print(f 'ingrese una palabra {cantidad_letras}letras')
    continue
else: 
   
#verificamos las palabras
 linea_verificada = verificar_palabra_ingresada
    (palabra_a_encontrar,palabra_ingresada grilla.append(linea_verificada))
    
    