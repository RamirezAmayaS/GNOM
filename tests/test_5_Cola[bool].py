def test_5_Colabool():
    candidato = []
    f = open('salidas/generador_arboles/5_Cola[bool].txt', 'r')
    for arbol in f:
        arbol = arbol.replace('\n','')
        candidato.append(arbol)

    solucion = []
    f = open('tests/soluciones/generador_arboles/5_Cola[bool].txt', 'r')
    for arbol in f:
        arbol = arbol.replace('\n','')
        solucion.append(arbol)

    assert sorted(candidato)==sorted(solucion)
