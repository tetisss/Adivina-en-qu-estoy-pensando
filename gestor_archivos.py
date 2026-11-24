#GESTOR DE ARCHIVOS

import os
from nodo import Nodo
from arbol import ArbolDecision


class GestorArchivos:

    def guardar(self, arbol, ruta):
        # E: arbol (ArbolDecision), ruta (str)
        # S: tupla (bool, str): si se guardó y un mensaje para el usuario
        
        try:
            lineas = []
            self.generar_lineas(arbol.raiz, lineas)
            archivo = open(ruta, "w", encoding="utf-8")
            archivo.write("\n".join(lineas) + "\n")
            archivo.close()
            return True, "Árbol guardado correctamente!."
        except OSError:
            return False, "No se pudo guardar correctamente."

    def generar_lineas(self, nodo, lineas):
        # E: nodo (Nodo), lineas (lista donde se van agregando las líneas)
        # S: ninguna

        if nodo.es_hoja():
            lineas.append("R|" + nodo.texto)
        else:
            lineas.append("P|" + nodo.texto)
            self.generar_lineas(nodo.si, lineas)
            self.generar_lineas(nodo.no, lineas)

    def cargar(self, ruta):
        # E: ruta (str)
        # S: tupla: el árbol (None si falló), y un mensaje para el usuario  
        
        if not os.path.exists(ruta):
            return None, "El archivo no existe"

        try:
            archivo = open(ruta, "r", encoding="utf-8-sig")
            contenido = archivo.read()
            archivo.close()
        except (OSError, UnicodeDecodeError):
            return None, "No se pudo leer el archivo"

        lineas = []
        for linea in contenido.split("\n"):
            if linea.strip() != "":
                lineas.append(linea.strip())

        if len(lineas) == 0:
            return None, "El archivo esta vacío"

        try:
            raiz, siguiente = self.construir(lineas, 0)
        except ValueError as error:
            return None, str(error)

        if siguiente != len(lineas):
            return None, "El archivo tiene líneas de más"

        return ArbolDecision(raiz), "Árbol cargado correctamente"

    def construir(self, lineas, i):
        # E: lineas, i (posición de la línea a leer)
        # S: tupla

        if i >= len(lineas):
            raise ValueError("A el archivo le faltan nodos")

        partes = lineas[i].split("|", 1)
        if len(partes) != 2 or partes[0] not in ("P", "R") or partes[1].strip() == "":
            raise ValueError("Formato incorrecto en la línea " + str(i + 1) + ".")

        tipo = partes[0]
        texto = partes[1].strip()

        if tipo == "R":
            return Nodo(texto), i + 1

        # Es pregunta: lo que sigue es la rama Sí y después la rama No
        hijo_si, i = self.construir(lineas, i + 1)
        hijo_no, i = self.construir(lineas, i)
        return Nodo(texto, hijo_si, hijo_no), i
