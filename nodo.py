#NODOS

class Nodo:
    #Representa un nodo del árbol

    def __init__(self, texto, si=None, no=None):
        # E: textol, Nodo o None
        # S: ninguna
        
        self.texto = texto
        self.si = si
        self.no = no

    def es_hoja(self):
        # E: ninguna
        # S: boolean

        return self.si is None and self.no is None

    
