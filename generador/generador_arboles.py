#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import itertools
import re
import os
from .TAD import TAD
from .estructuras_de_datos import Pila,Nodo,Arbol

# Procedimiento que construye un árbol a partir de su representación como paréntesis anidado
def parentesis_a_arbol_etiquetado(parentesis,etiquetas):
    # Stack para almacenar el último nodo abierto
    pila = Pila()
    raiz = Nodo(etiquetas[0])
    arbol = Arbol(raiz)
    pila.push(raiz)
    etiqueta = 1
    indice = 1
    while(indice < len(parentesis)-1):
        if pila.isEmpty():
            break
        elif parentesis[indice] == '(':
            ultimo_nodo = Nodo(etiquetas[etiqueta])
            pila.peek().add_child(ultimo_nodo)
            pila.push(ultimo_nodo)
            etiqueta = etiqueta + 1;
            indice = indice + 1
        else:
            pila.pop()
            indice = indice + 1;
    else:
        return arbol

    return Arbol(None)

# Procedimiento que devuelve el conjunto de etiquetas aptas para el árbol candidato
def generar_etiquetas(arbol,tad):
    if(not arbol.raiz):
        pass
    else:
        etiquetas = set()
        grado = len(arbol.raiz.children)
        aridades = tad.dar_aridad_generadoras()
        for nom,aridad in aridades.items():
            if(grado==aridad):
                if(grado==0):
                    etiquetas.add(nom)
                else:
                    etiquetas_temp = set()
                    etiquetas_temp.add(nom)
                    listas_etiquetas_hijos = [generar_etiquetas(Arbol(arbol.raiz.children[i]),instanciar_TAD(tad.generadoras[nom][i])) for i in list(range(grado))]
                    producto_etiquetas_hijos = [element for element in itertools.product(*listas_etiquetas_hijos)]
                    etiquetas_temp = list(itertools.product(etiquetas_temp,producto_etiquetas_hijos))
                    etiquetas = etiquetas.union(etiquetas_temp)

        return etiquetas

# Implementación en Python del algoritmo P (Knuth 2005)
# Generación de todos los paréntesis anidados en orden lexicográfico
def generar_arboles_aptos(n,tad,f):
    tiempo_inicio = time.time()
    #P1 - Inicializar
    a = [izquierdo if i % 2 == 1 else derecho for i in range(0,2*n+1)]
    m = 2*n-1
    finalizado = False
    total = 0;
    aptos = 0;
    #P2 - Visitar
    while not finalizado:
        total = total + 1
        candidato = ''.join(str(x) for x in a)[1:]

        #Evaluación de árbol candidato
        # Generación de todas las etiquetas
        etiquetas = generar_etiquetas(parentesis_a_arbol_etiquetado(candidato,list(' '*n)),tad)
        if etiquetas:
            # Generación de árboles representativos
            for etiqueta in etiquetas:
                etiqueta_lineal = []
                for tag in linealizar(etiqueta):
                    etiqueta_lineal.append(tag)
                arbol = parentesis_a_arbol_etiquetado(candidato,etiqueta_lineal)
                arbol_etiquetado = procesar(arbol.imprimir_arbol_etiquetado(''))
                print(arbol_etiquetado)
                f.write(arbol_etiquetado)
                f.write('\n')
                aptos = aptos + 1

        #P3 - Caso fácil?
        a[m] = derecho
        if a[m-1] == derecho:
            a[m-1] = izquierdo
            m = m-1
        else:
            #P4 - Encontrar j
            j = m-1
            k = 2*n-1
            while a[j] == izquierdo:
                a[j] = derecho
                a[k] = izquierdo
                j = j-1
                k = k-2
            #P5 - Incrementar a_{j}
            if j == 0:
                finalizado = True
            else:
                a[j] = izquierdo
                m = 2*n-1

    tiempo_total = time.time() - tiempo_inicio
    print(' ')
    print ('********************************** Se contaron %d árboles síntacticos en %f segundos ********************************' % (aptos,tiempo_total))
    print(' ')

def instanciar_TAD(signatura):
    # Parsing de signatura
    if signatura[0] == '[' and signatura[len(signatura)-1] == ']':
        signatura = signatura[1:-1]
    split_signatura = signatura.split('[',1)
    nombre = split_signatura[0]
    if len(split_signatura) > 1:
        parametro = split_signatura[1][:-1]
        parametros = parse_exp_parametros(parametro)
    else:
        parametros = []

    tad = TAD(nombre=nombre,es_basico=False,parametros=parametros)

    #Especificación de Tipos Abstractos de Datos
    if nombre == 'Cola':
        tad.anadir_generadora('vac_cola',())
        # Creación de generadoras articiales
        for param in parametros:
            tad.anadir_generadora('ins_' + param.split('[')[0][0:3],('Cola[' + parametro + ']','[' + param + ']'))

    elif nombre == 'DCola':
        tad.anadir_generadora('vac_dcola',())
        # Creación de generadoras articiales
        for param in parametros:
            tad.anadir_generadora('ins_der_' + param.split('[')[0][0:3],('DCola[' + parametro + ']','[' + param + ']'))
            tad.anadir_generadora('ins_izq_' + param.split('[')[0][0:3],('[' + param + ']','DCola[' + parametro + ']'))

    elif nombre == 'Arbin':
        tad.anadir_generadora('vac_arbin',())
        # Creación de generadoras articiales
        for param in parametros:
            tad.anadir_generadora('cons_' + param.split('[')[0][0:3],('Arbin[' + parametro + ']','[' + param + ']','Arbin[' + parametro + ']'))

    # Especificación de Tipos Primitivos Finitos
    elif nombre.startswith('bool'):
        tad.anadir_generadora(nombre,())

    elif nombre.startswith('nat'):
        tad.anadir_generadora(nombre,())

    elif nombre.startswith('int'):
        tad.anadir_generadora(nombre,())

    return tad

# Procedimiento para definir los parámetros de un TAD a partir de su expresión anidada.
def parse_exp_parametros(exp_parametros):
    pila = []
    pos_parametros = [0]
    for i,c in enumerate(exp_parametros):
        if c == '[':
            pila.append(i)
        elif c == ']' and pila:
            pila.pop()
        elif c == ',' and not pila:
            pos_parametros.append(i)

    parametros = []
    if len(pos_parametros) > 1:
        for i in list(range(1,len(pos_parametros))):
            parametros.append(exp_parametros[pos_parametros[i-1]:pos_parametros[i]].replace(',',''))
        parametros.append(exp_parametros[pos_parametros[len(pos_parametros)-1]:len(exp_parametros)].replace(',',''))
    else:
        parametros.append(exp_parametros)

    return parametros

# Procedimiento para reemplazar etiquetas de generadoras artificiales
def procesar(arbol_etiquetado):
    arbol_etiquetado = arbol_etiquetado.replace('ins_nat','ins')
    arbol_etiquetado = arbol_etiquetado.replace('ins_int','ins')
    arbol_etiquetado = arbol_etiquetado.replace('ins_boo','ins')
    arbol_etiquetado = arbol_etiquetado.replace('ins_Col','ins')
    arbol_etiquetado = arbol_etiquetado.replace('ins_DCo','ins')
    arbol_etiquetado = arbol_etiquetado.replace('ins_Arb','ins')

    arbol_etiquetado = arbol_etiquetado.replace('ins_der_nat','ins_der')
    arbol_etiquetado = arbol_etiquetado.replace('ins_der_int','ins_der')
    arbol_etiquetado = arbol_etiquetado.replace('ins_der_boo','ins_der')
    arbol_etiquetado = arbol_etiquetado.replace('ins_der_Col','ins_der')
    arbol_etiquetado = arbol_etiquetado.replace('ins_der_DCo','ins_der')
    arbol_etiquetado = arbol_etiquetado.replace('ins_der_Arb','ins_der')
    arbol_etiquetado = arbol_etiquetado.replace('ins_izq_nat','ins_izq')
    arbol_etiquetado = arbol_etiquetado.replace('ins_izq_int','ins_izq')
    arbol_etiquetado = arbol_etiquetado.replace('ins_izq_boo','ins_izq')
    arbol_etiquetado = arbol_etiquetado.replace('ins_izq_Col','ins_izq')
    arbol_etiquetado = arbol_etiquetado.replace('ins_izq_DCo','ins_izq')
    arbol_etiquetado = arbol_etiquetado.replace('ins_izq_Arb','ins_izq')

    arbol_etiquetado = arbol_etiquetado.replace('cons_nat','cons')
    arbol_etiquetado = arbol_etiquetado.replace('cons_int','cons')
    arbol_etiquetado = arbol_etiquetado.replace('cons_boo','cons')
    arbol_etiquetado = arbol_etiquetado.replace('cons_Col','cons')
    arbol_etiquetado = arbol_etiquetado.replace('cons_DCo','cons')
    arbol_etiquetado = arbol_etiquetado.replace('cons_Arb','cons')

    return arbol_etiquetado

# Procedimientos instrumentales para linealizar una tupla
def lista_o_tupla(t):
    return isinstance(t, (list, tuple))

def linealizar(secuencia, exp=lista_o_tupla):
    for elemento in secuencia:
        if exp(elemento):
            for sub in linealizar(elemento, exp):
                yield sub
        else:
            yield elemento

# Procedimiento principal
def generar_arboles(nodos,tad):

    global izquierdo
    izquierdo = '('
    global derecho
    derecho = ')'
    n = int(nodos)
    global signatura
    signatura = tad
    print('')

    try:
        f = open(os.path.join(sys.path[0], 'salidas/generador_arboles/%s' % str(n) + '_' + signatura + '.txt'), 'x')
        print('************* El conjunto de árboles sintácticos con %d nodos aptos para representar nombres en %s es: *************' % (int(n),signatura))
        print('')
        tad = instanciar_TAD(signatura)
        generar_arboles_aptos(n,tad,f)
    except FileExistsError:
        print('El conjunto de árboles sintácticos con %d nodos para %s ya fue generado. Se encuentra en ./salidas/generador_arboles/%d_%s \n' % (n,signatura,n,signatura))
