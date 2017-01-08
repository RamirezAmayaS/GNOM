# -*- coding: utf-8 -*-

from .generador_arboles import generar_arboles
from. generador_nombres import generar_nombres

print(" ")
print("name = GNom")
print("version = 1.0")
print("author = Simón Ramírez Amaya")
print("author-email = s.ramirez34@uniandes.edu.co")
print(" ")
print("Bienvenido a GNom!")
print(" ")
funcionalidad = input("Por favor indique si desea generar árboles sintácticos (A) o generar una muestra de nombres (N) : ")
print(" ")
if(funcionalidad=='A'):
    n = input("Indique el tamaño de los árboles a generar: ")
    especificacion = input("Especifique el Tipo Abstracto de Dato: ")
    generar_arboles(n,especificacion)
elif(funcionalidad=='N'):
    n = input("Indique el tamaño de los árboles generados: ")
    especificacion = input("Especifique el Tipo Abstracto de Dato: ")
    m = input("Indique el tamaño de la muestra a generar: ")
    h = input("Indique si desea generar un histograma para la muestra (N/S): ")
    generar_nombres(n,especificacion,m,h)
