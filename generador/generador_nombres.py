#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import random
import time
import os
import collections
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np

def leer_arboles(f):
    arboles = {}
    for arbol in f:
        arbol = arbol.replace('\n','')
        representatividad = calcular_representatividad(arbol)
        arboles[arbol] = representatividad

    return arboles

def calcular_representatividad(arbol):
    representatividad = 1
    placeholders_at = [m.start() for m in re.finditer('@',arbol)]
    for i,at in enumerate(placeholders_at):
        if i%2 == 0:
            split = arbol[placeholders_at[i]+1:placeholders_at[i+1]].split(':')
            a = int(split[0])
            b = int(split[1])
            tamano = b-a+1
            representatividad = representatividad*tamano

    placeholders_bool = [m.start() for m in re.finditer('bool',arbol)]
    if len(placeholders_bool) > 0:
        representatividad = representatividad*2**len(placeholders_bool)

    return representatividad

def elegir_arbol(arboles):
    r = random.uniform(0, sum(arboles.values()))
    suma_parcial = 0.0
    for arbol,representatividad in arboles.items():
        suma_parcial = suma_parcial + representatividad
        if r < suma_parcial:
            return arbol

def instanciar_nombre(arbol):
    nombre_temp = ''
    pos = 0
    placeholders_at = [m.start() for m in re.finditer('@',arbol)]
    for i,at in enumerate(placeholders_at):
        if i%2 == 0:
            split = arbol[placeholders_at[i]+1:placeholders_at[i+1]].split(':')
            a = int(split[0])
            b = int(split[1])
            nombre_temp = nombre_temp + arbol[pos:placeholders_at[i]-3] + str(random.randint(a,b))
            pos = placeholders_at[i + 1] + 1
    if placeholders_at:
        nombre_temp = nombre_temp + arbol[placeholders_at[-1]+1:len(arbol)]
    else:
        nombre_temp = arbol

    nombre = ''
    pos = 0
    placeholders_bool = [m.start() for m in re.finditer('bool',nombre_temp)]
    for i,bo in enumerate(placeholders_bool):
        nombre = nombre + nombre_temp[pos:placeholders_bool[i]] + str(random.choice([True, False])).lower()
        pos = placeholders_bool[i] + 4
    if placeholders_bool:
        nombre = nombre + nombre_temp[placeholders_bool[-1]+4:len(nombre_temp)]
    else:
        nombre = nombre_temp
    return nombre

def generar_muestra(arboles,m):
    f = open(os.path.join(sys.path[0],'salidas/generador_nombres/%s' % str(n) + '_' + signatura + time.strftime("%Y%m%d-%H:%M:%S") + '.txt'), 'x')
    frecuencia_muestra = collections.defaultdict(lambda:0)
    for i in list(range(m)):
        arbol = elegir_arbol(arboles)
        nombre = instanciar_nombre(arbol)
        f.write(nombre)
        f.write('\n')
        print(nombre)
        frecuencia_muestra[nombre] += 1
    if hist == 'S':
        mostrar_histograma(arbol,frecuencia_muestra)

def mostrar_histograma(arbol,frecuencia_muestra):
    x = np.arange(len(frecuencia_muestra))
    pl.bar(x, frecuencia_muestra.values(), align='center', width=0.5)
    pl.xlabel("Nombres en Y[X]",fontsize=18)
    pl.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
    pl.ylabel("Frecuencia muestral",fontsize=18)
    ymax = max(frecuencia_muestra.values()) + max(frecuencia_muestra.values())/10
    pl.ylim(0, ymax)
    pl.suptitle('n=%d, m=%d, Y[X]=%s' % (n,m,signatura))
    plt.savefig('salidas/hists/%s' % str(n) + '_' + signatura + '_' + str(m))
    pl.show()

def generar_nombres(nodos,tad,muestra,h):

    global n
    n = int(nodos)
    global signatura
    signatura = tad
    global hist
    hist = h
    global m
    m = int(muestra)
    print('')

    try:
        str(n) + '_' + signatura + '.txt'
        f = open('salidas/generador_arboles/%s' % str(n) + '_' + signatura + '.txt', 'r')
        print('************* La muestra de tamaño %d de nombres en %s representables a partir de árboles sintácticos con %d nodos es: *************' % (m,signatura,n))
        print('')
        arboles = leer_arboles(f)
        generar_muestra(arboles,m)
        print('')
        print('***************** Se contaron %d nombres en %s representables a partir de árboles sintácticos con %d nodos.  ******************' % (sum(arboles.values()),signatura,n))
        print('')
        time.sleep(1)
    except FileNotFoundError:
        print('El conjunto de árboles sintácticos con %d nodos para %s no ha sido generado. Utilice el generador de árboles.\n' % (n,signatura))
