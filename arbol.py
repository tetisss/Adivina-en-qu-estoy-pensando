#ARBOL

from nodo import Nodo


class ArbolDecision:
    """Guarda la raíz del árbol y se encarga de que crezca."""

    def __init__(self, raiz=None):
        # E: raiz (Nodo o None)
        # S: ninguna
        
        if raiz is None:
            raiz = self.crear_por_defecto()
        self.raiz = raiz

    def crear_por_defecto(self):
        # E: ninguna
        # S: un Nodo raíz

        return Nodo("¿Es un animal?", Nodo("Perro"), Nodo("Computadora"))

    def aprender(self, hoja, respuesta_nueva, pregunta, es_si):
        # E: hoja, respuesta_nueva, pregunta, es_si (boolean)
        # S: True si aprendió, False si algún dato no es válido

        respuesta_nueva = respuesta_nueva.strip()
        pregunta = pregunta.strip()
        if not hoja.es_hoja() or respuesta_nueva == "" or pregunta == "":
            return False

        vieja = Nodo(hoja.texto)      # copia de la respuesta incorrecta
        nueva = Nodo(respuesta_nueva)

        hoja.texto = pregunta         # la hoja pasa a ser nodo de pregunta
        if es_si:
            hoja.si, hoja.no = nueva, vieja
        else:
            hoja.si, hoja.no = vieja, nueva
        return True

    def contar_nodos(self, nodo=None, es_raiz=True):
        # E: nodo, es_raiz (bool)
        # S: cantidad total de nodos

        if es_raiz:
            nodo = self.raiz
        if nodo is None:
            return 0
        return 1 + self.contar_nodos(nodo.si, False) + self.contar_nodos(nodo.no, False)
