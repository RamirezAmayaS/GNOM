# -*- coding: utf-8 -*-

# Implementación general de un Stack
class Pila:
    def __init__(self):
         self.items = []

    def isEmpty(self):
         return self.items == []

    def push(self, item):
         self.items.append(item)

    def pop(self):
         return self.items.pop()

    def peek(self):
         return self.items[len(self.items)-1]

    def size(self):
         return len(self.items)

# Implementación general de un nodo de un árbol
class Nodo(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

# Implementación general de un árbol
class Arbol(object):
    def __init__(self,raiz):
        self.raiz = raiz

    def imprimir_arbol_etiquetado(self,representacion):
        rep = representacion + str(self.raiz.data)
        #print(self.raiz.data,end='')
        rep = rep + '('
        #print('(',end='')
        if(len(self.raiz.children)==0):
            rep = rep + ')'
            #print(')',end='')
        else:
            for hijo in self.raiz.children:
                rep = rep + Arbol(hijo).imprimir_arbol_etiquetado('')
            rep = rep + ')'
            #print (')',end='')
        return rep
