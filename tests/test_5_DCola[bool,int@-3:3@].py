def test_5_Colaboolint33():
    candidato = []
    f = open('salidas/generador_arboles/5_DCola[bool,int@-3:3@].txt', 'r')
    for arbol in f:
        arbol = arbol.replace('\n','')
        candidato.append(arbol)

    solucion = []
    f = open('tests/soluciones/generador_arboles/5_DCola[bool,int@-3:3@].txt', 'r')
    for arbol in f:
        arbol = arbol.replace('\n','')
        solucion.append(arbol)

    assert sorted(candidato)==sorted(solucion)
