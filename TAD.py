class TAD(object):

    def __init__(self,nombre,es_basico):
        self.nombre = nombre
        self.es_basico = es_basico
        self.generadoras = {}

    def anadir_generadora(self,nombre,dominio):
        self.generadoras[nombre] = dominio

    def dar_aridad_generadoras(self):
        aridad = {}
        for nombre,dominio in self.generadoras.items():
            aridad[nombre] = len(dominio)
        return aridad

    def __str__(self):
        return "TAD con nombre %s, parámetros %s y generadoras %s. Es básico? %s" % (self.nombre, self.parametros, self.generadoras, self.es_basico)
