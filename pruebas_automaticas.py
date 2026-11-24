# PRUEBAS AUTOMÁTICAS

import os
from arbol import ArbolDecision
from partida import Partida
from gestor_archivos import GestorArchivos

errores = 0


def verificar(descripcion, obtenido, esperado):
    # Imprime OK si ambos valores son iguales, o ERROR con los dos valores
    global errores
    if obtenido == esperado:
        print("OK     ", descripcion)
    else:
        errores += 1
        print("ERROR  ", descripcion, "| obtenido:", obtenido, "| esperado:", esperado)


def escribir(ruta, texto):
    archivo = open(ruta, "w", encoding="utf-8")
    archivo.write(texto)
    archivo.close()


# =====================================================
# ARBOL: estado inicial
# =====================================================
print("\n--- Estado inicial ---")
a = ArbolDecision()
verificar("raíz por defecto", a.raiz.texto, "¿Es un animal?")
verificar("hoja Sí es Perro", a.raiz.si.texto, "Perro")
verificar("hoja No es Computadora", a.raiz.no.texto, "Computadora")
verificar("Perro es hoja", a.raiz.si.es_hoja(), True)
verificar("la raíz no es hoja", a.raiz.es_hoja(), False)
verificar("nodos iniciales", a.contar_nodos(), 3)

# =====================================================
# ARBOL: aprendizaje (partidas 2 a 5 del anexo)
# =====================================================
print("\n--- Aprendizaje ---")
verificar("aprender Gato", a.aprender(a.raiz.si, "Gato", "¿Maúlla?", True), True)
verificar("pregunta nueva", a.raiz.si.texto, "¿Maúlla?")
verificar("Sí -> Gato", a.raiz.si.si.texto, "Gato")
verificar("No -> Perro", a.raiz.si.no.texto, "Perro")
verificar("nodos tras Gato", a.contar_nodos(), 5)

a.aprender(a.raiz.si.no, "Águila", "¿Puede volar?", True)
verificar("nodos tras Águila", a.contar_nodos(), 7)

a.aprender(a.raiz.no, "Carro", "¿Sirve para transportarse?", True)
verificar("nodos tras Carro", a.contar_nodos(), 9)

a.aprender(a.raiz.si.no.no, "Delfín", "¿Vive en el agua?", True)
verificar("nodos tras Delfín", a.contar_nodos(), 11)
verificar("Delfín en rama Sí", a.raiz.si.no.no.si.texto, "Delfín")
verificar("Perro en rama No", a.raiz.si.no.no.no.texto, "Perro")

print("\n--- Respuesta nueva en la rama No ---")
b = ArbolDecision()
b.aprender(b.raiz.si, "Pez", "¿Vive en el agua?", False)
verificar("nueva en rama No", b.raiz.si.no.texto, "Pez")
verificar("anterior se conserva en Sí", b.raiz.si.si.texto, "Perro")

# =====================================================
# ARBOL: validaciones (el árbol no debe cambiar)
# =====================================================
print("\n--- Validaciones de aprender ---")
c = ArbolDecision()
verificar("respuesta vacía", c.aprender(c.raiz.si, "", "¿Maúlla?", True), False)
verificar("pregunta vacía", c.aprender(c.raiz.si, "Gato", "", True), False)
verificar("solo espacios", c.aprender(c.raiz.si, "   ", "   ", True), False)
verificar("nodo que no es hoja", c.aprender(c.raiz, "Gato", "¿Maúlla?", True), False)
verificar("nodos sin cambios", c.contar_nodos(), 3)
verificar("Perro sigue en su lugar", c.raiz.si.texto, "Perro")

# =====================================================
# PARTIDA: recorrido
# =====================================================
print("\n--- Partida: recorrido ---")
p = Partida(ArbolDecision())
verificar("empieza en la raíz", p.texto_actual(), "¿Es un animal?")
verificar("raíz no es hoja", p.es_hoja(), False)
verificar("responder Sí avanza", p.responder(True), True)
verificar("llegó a hoja", p.es_hoja(), True)
verificar("texto de adivinar", p.texto_actual(), "¿Estabas pensando en Perro?")
verificar("no avanza desde hoja", p.responder(True), False)
p.reiniciar()
verificar("reiniciar vuelve a la raíz", p.texto_actual(), "¿Es un animal?")
p.responder(False)
verificar("rama No", p.texto_actual(), "¿Estabas pensando en Computadora?")

# =====================================================
# PARTIDA: aprender
# =====================================================
print("\n--- Partida: aprender ---")
p = Partida(ArbolDecision())
p.responder(True)
verificar("partida aprende", p.aprender("Gato", "¿Maúlla?", True), True)
p.reiniciar()
p.responder(True)
verificar("nueva pregunta en el camino", p.texto_actual(), "¿Maúlla?")
p.responder(True)
verificar("llega a Gato", p.texto_actual(), "¿Estabas pensando en Gato?")

# =====================================================
# GESTOR DE ARCHIVOS: guardar y cargar
# =====================================================
print("\n--- Archivos: guardar y cargar ---")
g = GestorArchivos()

verificar("guardar", g.guardar(a, "prueba_guardado.txt")[0], True)
cargado, mensaje = g.cargar("prueba_guardado.txt")
verificar("cargar devuelve árbol", cargado is not None, True)
verificar("mismos nodos", cargado.contar_nodos(), 11)
lineas_a = []
g.generar_lineas(a.raiz, lineas_a)
lineas_c = []
g.generar_lineas(cargado.raiz, lineas_c)
verificar("misma estructura", lineas_c, lineas_a)

# =====================================================
# GESTOR DE ARCHIVOS: errores al cargar
# =====================================================
print("\n--- Archivos: errores al cargar ---")
verificar("no existe", g.cargar("no_existe.txt")[0], None)
print("   mensaje:", g.cargar("no_existe.txt")[1])

escribir("vacio.txt", "")
verificar("vacío", g.cargar("vacio.txt")[0], None)
print("   mensaje:", g.cargar("vacio.txt")[1])

escribir("malo.txt", "hola esto no es un árbol\n")
verificar("formato incorrecto", g.cargar("malo.txt")[0], None)
print("   mensaje:", g.cargar("malo.txt")[1])

escribir("incompleto.txt", "P|¿Es un animal?\nR|Perro\n")
verificar("incompleto", g.cargar("incompleto.txt")[0], None)
print("   mensaje:", g.cargar("incompleto.txt")[1])

escribir("sobran.txt", "R|Perro\nR|Gato\n")
verificar("líneas de más", g.cargar("sobran.txt")[0], None)
print("   mensaje:", g.cargar("sobran.txt")[1])

# =====================================================
# Limpieza de archivos temporales y resumen
# =====================================================
for nombre in ["prueba_guardado.txt", "vacio.txt", "malo.txt", "incompleto.txt", "sobran.txt"]:
    if os.path.exists(nombre):
        os.remove(nombre)

print()
if errores == 0:
    print("TODAS LAS PRUEBAS PASARON")
else:
    print("HAY", errores, "PRUEBA(S) CON ERROR")
