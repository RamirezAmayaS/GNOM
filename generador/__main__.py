# -*- coding: utf-8 -*-

from .generador_arboles import generar_arboles
from. generador_nombres import generar_nombres

print(" ")
print("Ejecutando versión 1.0 de GNOM...")
print(" ")
funcionalidad = input("Bienvenido a GNOM. Por favor indique si desea generar árboles sintácticos (A) o generar una muestra de nombres (N) : ")
print(" ")
if(funcionalidad=='A'):
    n = input("Indique el tamaño de los árboles a generar: ")
    especificacion = input("Especifique el Tipo Abstracto de Dato: ")
    generar_arboles(n,especificacion)
elif(funcionalidad=='N'):
    n = input("Indique el tamaño de los árboles generados: ")
    especificacion = input("Especifique el Tipo Abstracto de Dato: ")
    m = input("Indique el tamaño de la muestra a generar: ")
    generar_nombres(n,especificacion,m)
