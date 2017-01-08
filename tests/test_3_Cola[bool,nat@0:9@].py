def test_3_Colaboolnat09():
    candidato = []
    f = open('salidas/generador_arboles/3_Cola[bool,nat@0:9@].txt', 'r')
    for arbol in f:
        arbol = arbol.replace('\n','')
        candidato.append(arbol)

    solucion = []
    f = open('tests/soluciones/generador_arboles/3_Cola[bool,nat@0:9@].txt', 'r')
    for arbol in f:
        arbol = arbol.replace('\n','')
        solucion.append(arbol)

    assert sorted(candidato)==sorted(solucion)
