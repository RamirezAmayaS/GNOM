#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import itertools
from TAD import TAD
from estructuras_de_datos import Pila,Nodo,Arbol

# Procedimiento que construye un árbol a partir de su representación como paréntesis anidado y lo etiqueta
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
def generar_arboles_aptos(n,tad):
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
        etiquetas = generar_etiquetas(parentesis_a_arbol_etiquetado(candidato,list(' '*n)),tad)
        if etiquetas:
            for etiqueta in etiquetas:
                etiqueta_lineal = []
                for tag in flatten(etiqueta):
                    etiqueta_lineal.append(tag)
                arbol = parentesis_a_arbol_etiquetado(candidato,etiqueta_lineal)
                arbol.imprimir_arbol_etiquetado()
                print(' ')
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
    print ('********************************** Se contaron %d árboles aptos en %f segundos ********************************' % (aptos,tiempo_total))
    print(' ')

def instanciar_TAD(signatura):
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
        for param in parametros:
            tad.anadir_generadora('ins_' + param.split('[')[0],('Cola[' + parametro + ']','[' + param + ']'))

    elif nombre == 'DCola':
        tad.anadir_generadora('vac_dcola',())
        for param in parametros:
            tad.anadir_generadora('ins_der_' + param.split('[')[0],('DCola[' + parametro + ']','[' + param + ']'))
            tad.anadir_generadora('ins_izq_' + param.split('[')[0],('[' + param + ']','DCola[' + parametro + ']'))

    elif nombre == 'Arbin':
        tad.anadir_generadora('vac_arbin',())
        for param in parametros:
            tad.anadir_generadora('cons_',('Arbin[' + parametro + ']','[' + param + ']','Arbin[' + parametro + ']'))
            #tad.anadir_generadora('cons_' + param.split('[')[0],('Arbin[' + parametro + ']','[' + param + ']','Arbin[' + parametro + ']'))

    # Especificación de Tipos Primitivos

    elif nombre.startswith('bool'):
        tad.anadir_generadora(nombre,())

    elif nombre.startswith('nat'):
        tad.anadir_generadora(nombre,())

    elif nombre.startswith('int'):
        tad.anadir_generadora(nombre,())

    return tad

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

def list_or_tuple(x):
    return isinstance(x, (list, tuple))

def flatten(sequence, to_expand=list_or_tuple):
    for item in sequence:
        if to_expand(item):
            for subitem in flatten(item, to_expand):
                yield subitem
        else:
            yield item

if __name__ == "__main__":
    izquierdo = '('
    derecho = ')'
    nodos = int(sys.argv[1])
    signatura = sys.argv[2]
    print('')
    print('************* El conjunto de árboles etiquetados aptos para representar nombres en %s es: *************' % signatura)
    print('')
    tad = instanciar_TAD(signatura)
    generar_arboles_aptos(nodos,tad)
