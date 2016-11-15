# -*- coding: utf-8 -*-

def lista_ins_derecha(*x):
    funcs = {"vac":(),"ins":("lista_ins_derecha[" + ''.join(x) + "]",''.join(x))}
    return funcs

def lista_ins_izquierda(*x):
    funcs = {"vac":(),"ins":(''.join(x),"lista_ins_izquierda[" + ''.join(x) + "]")}
    return funcs

def lista_ins_derecha_izquierda(*x):
    funcs = {"vac":(),
                "ins_der":("lista_ins_derecha_izquierda[" + ''.join(x) + "]",''.join(x)),
                    "ins_izq":(''.join(x),"lista_ins_derecha_izquierda[" + ''.join(x) + "]")}
    return funcs

def nat_entre_1_y_5(*x):
    funcs = {"1":(),"2":(),"3":(),"4":(),"5":()}
    return funcs
