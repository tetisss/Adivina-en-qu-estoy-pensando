#PARTIDA

from arbol import ArbolDecision


class Partida:
    """Lleva el recorrido de una partida sobre un árbol de decisión."""

    def __init__(self, arbol):
        # E: arbol 
        # S: ninguna

        self.arbol = arbol
        self.actual = arbol.raiz

    def reiniciar(self):
        # Vuelve a la raíz para empezar otra partida
        
        self.actual = self.arbol.raiz

    def es_hoja(self):
        # E: ninguna
        # S: True si el nodo actual es una respuesta final, False si es pregunta

        return self.actual.es_hoja()

    def texto_actual(self):
        # E: ninguna
        # S: el texto que se le muestra al usuario
        # Si es hoja, pregunta si pensaba en esa respuesta; si no, es la pregunta
        
        if self.actual.es_hoja():
            return "¿Estabas pensando en " + self.actual.texto + "?"
        return self.actual.texto

    def responder(self, es_si):
        # E: es_si (bool)
        # S: boolean (true si avanzo, false si no)

        if self.actual.es_hoja():
            return False
        if es_si:
            self.actual = self.actual.si
        else:
            self.actual = self.actual.no
        return True

    def aprender(self, respuesta_nueva, pregunta, es_si):
        # E: respuesta_nueva, pregunt, es_si (boolean)
        # S: True si el árbol aprendió, False si algún dato no es válido

        return self.arbol.aprender(self.actual, respuesta_nueva, pregunta, es_si)
