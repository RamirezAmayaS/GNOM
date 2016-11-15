#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import tads
from data_structures import Stack,Node

# Procedimiento que construye un árbol a partir de su representación como paréntesis anidado
def parenthesis_to_tree(parenthesis):
    # Stack para almacenar el último nodo abierto
    stack = Stack()
    root = Node('raiz')
    stack.push(root)
    index = 1
    while(index < len(parenthesis)-1):
        if stack.isEmpty():
            break
        elif parenthesis[index] == '(':
            last_opened_node = Node('posicion' + str(index))
            stack.peek().add_child(last_opened_node)
            stack.push(last_opened_node)
            index = index + 1
        else:
            stack.pop()
            index = index + 1;
    else:
        return root

    return Node('not a rooted tree')

# Procedimiento que evalúa la aptitud de un árbol para representar una instancia de un TAD
def check_fitness(node,TAD):
    if node.data == 'not a rooted tree':
        return False
    else:
        TAD_parse = TAD.split('[',1)
        TAD_call = getattr(tads,TAD_parse[0])
        TAD_funcs = TAD_call(TAD_parse[1][:-1])

        for tag,func in TAD_funcs.iteritems():
            if len(func) == len(node.children):
                for i,ptad in enumerate(func):
                    if check_fitness(node.children[i],ptad):
                        pass
                    else:
                        break
                else:
                    node.data = tag
                    print node.data
                    return True
        else:
            return None


# Python implementation of Algorithm P (Knuth 2005)
# Nested parenthesis generation in lexicographic order
def generate_all_fit_trees(n,TAD):
    start_time = time.time()
    #P1 - Initialize
    a = [izquierdo if i % 2 == 1 else derecho for i in range(0,2*n+1)]
    m = 2*n-1
    done = False
    total = 0;
    aptos = 0;
    #P2 - Visit
    while not done:
        total = total + 1
        candidato = ''.join(str(x) for x in a)[1:]
        print ' '
        if check_fitness(parenthesis_to_tree(candidato),TAD):
            print candidato
            print ' '
            aptos = aptos + 1
        #P3 - Easy case?
        a[m] = derecho
        if a[m-1] == derecho:
            a[m-1] = izquierdo
            m = m-1
        else:
            #P4 - Find j
            j = m-1
            k = 2*n-1
            while a[j] == izquierdo:
                a[j] = derecho
                a[k] = izquierdo
                j = j-1
                k = k-2
            #P5 - Increase a_{j}
            if j == 0:
                done = True
            else:
                a[j] = izquierdo
                m = 2*n-1

    elapsed_time = time.time() - start_time

    print "************* Se contaron %d árboles aptos de %d árboles en %f segundos *************" % (aptos,total,elapsed_time)

if __name__ == "__main__":
    izquierdo = '('
    derecho = ')'
    TAD = sys.argv[2]
    generate_all_fit_trees(int(sys.argv[1]),TAD)
