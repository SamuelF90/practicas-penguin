#BASE DE DATOS DE CONOCIMIENTOS CON PYDATALOG

from pyDatalog import pyDatalog

pyDatalog.clear()

# Hechos
pyDatalog.create_terms('animal, mamifero,anfibio, tiene_pelo,tiene_veneno, X')

+animal('perro')
+animal('gato')
+animal('serpiente')

+mamifero('perro')
+mamifero('gato')
+anfibio('serpiente')

# Regla
tiene_pelo(X) <= mamifero(X)
tiene_veneno(X)<= anfibio(X)

# Consultas
print("¿Tiene pelo el gato?")
print(tiene_pelo('gato'))  # Resultado: gato tiene pelo

print("¿Qué animales tienen pelo?")
print(tiene_pelo(X))  # Resultado: perro y gato

print("¿Qué animales tienen veneno?")
print(tiene_veneno(X))  # Resultado: serpiente
