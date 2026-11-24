import tkinter as tk
from tkinter import filedialog, messagebox
from arbol import ArbolDecision
from partida import Partida
from gestor_archivos import GestorArchivos

RUTA_POR_DEFECTO = "arbol_guardado.txt"


class Interfaz:
    """Ventana principal. Solo muestra información y llama a las otras clases."""

    def __init__(self, ventana):
        # E: ventana (tk.Tk)
        # S: ninguna
        
        self.ventana = ventana
        self.ventana.title("Adivina en qué estoy pensando")
        self.ventana.geometry("540x420")

        self.gestor = GestorArchivos()
        self.arbol = ArbolDecision()
        self.partida = Partida(self.arbol)
        self.ruta = RUTA_POR_DEFECTO      # archivo donde se guarda lo aprendido

        self.crear_pantalla_inicio()
        self.crear_pantalla_juego()
        self.crear_pantalla_aprendizaje()
        self.mostrar(self.frame_inicio)

    def crear_pantalla_inicio(self):
        #CREAR PANTALLA DE INICIO

        self.frame_inicio = tk.Frame(self.ventana, padx=20, pady=20)

        tk.Label(self.frame_inicio, text="Adivina en qué estoy pensando",
                 font=("Arial", 18, "bold")).pack(pady=(10, 15))
        tk.Label(self.frame_inicio, justify="center", wraplength=460,
                 text="Piensa en algo y responde mis preguntas con Sí o No. "
                      "Intentaré adivinarlo. Si fallo, me enseñas y aprendo "
                      "para la próxima vez.").pack(pady=10)

        self.label_estado = tk.Label(self.frame_inicio, fg="gray",
                                     text="Usando el árbol por defecto.")
        self.label_estado.pack(pady=10)

        tk.Button(self.frame_inicio, text="Iniciar partida", width=22,
                  command=self.iniciar_partida).pack(pady=4)
        tk.Button(self.frame_inicio, text="Cargar árbol desde archivo", width=22,
                  command=self.cargar_archivo).pack(pady=4)
        tk.Button(self.frame_inicio, text="Salir", width=22,
                  command=self.ventana.destroy).pack(pady=4)

    def crear_pantalla_juego(self):
        #CREAR PANTALLA PARA JUGAR
        self.frame_juego = tk.Frame(self.ventana, padx=20, pady=20)

        self.label_pregunta = tk.Label(self.frame_juego, font=("Arial", 16),
                                       wraplength=480, justify="center")
        self.label_pregunta.pack(pady=(30, 25))

        self.frame_respuestas = tk.Frame(self.frame_juego)
        tk.Button(self.frame_respuestas, text="Sí", width=10,
                  command=lambda: self.responder(True)).pack(side="left", padx=10)
        tk.Button(self.frame_respuestas, text="No", width=10,
                  command=lambda: self.responder(False)).pack(side="left", padx=10)

        self.frame_final = tk.Frame(self.frame_juego)
        tk.Button(self.frame_final, text="Nueva partida", width=14,
                  command=self.iniciar_partida).pack(side="left", padx=10)
        tk.Button(self.frame_final, text="Menú", width=14,
                  command=self.ir_a_inicio).pack(side="left", padx=10)
        tk.Button(self.frame_final, text="Salir", width=14,
                  command=self.ventana.destroy).pack(side="left", padx=10)

    def crear_pantalla_aprendizaje(self):
        #CREAR PANTALLA PARA APRENDIZAJE DEL ARBOL
        self.frame_aprender = tk.Frame(self.ventana, padx=20, pady=20)

        tk.Label(self.frame_aprender, text="Me rindo, ¡enséñame!",
                 font=("Arial", 16, "bold")).pack(pady=(5, 15))

        tk.Label(self.frame_aprender, text="¿En qué estabas pensando?").pack(anchor="w")
        self.entrada_respuesta = tk.Entry(self.frame_aprender, width=55)
        self.entrada_respuesta.pack(pady=(2, 12))

        self.label_diferenciar = tk.Label(self.frame_aprender, wraplength=480,
                                          justify="left")
        self.label_diferenciar.pack(anchor="w")
        self.entrada_pregunta = tk.Entry(self.frame_aprender, width=55)
        self.entrada_pregunta.pack(pady=(2, 12))

        tk.Label(self.frame_aprender,
                 text="Para tu respuesta, la respuesta a esa pregunta es:").pack(anchor="w")
        self.var_es_si = tk.StringVar(value="")      # "" = todavía no eligió
        marco = tk.Frame(self.frame_aprender)
        marco.pack(anchor="w", pady=(2, 12))
        tk.Radiobutton(marco, text="Sí", variable=self.var_es_si,
                       value="si").pack(side="left", padx=(0, 15))
        tk.Radiobutton(marco, text="No", variable=self.var_es_si,
                       value="no").pack(side="left")

        botones = tk.Frame(self.frame_aprender)
        botones.pack(pady=10)
        tk.Button(botones, text="Guardar", width=12,
                  command=self.guardar_aprendizaje).pack(side="left", padx=8)
        tk.Button(botones, text="Cancelar", width=12,
                  command=self.ir_a_inicio).pack(side="left", padx=8)

    def mostrar(self, frame):
        # E: frame (tk.Frame)
        # S: ninguna

        for f in (self.frame_inicio, self.frame_juego, self.frame_aprender):
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def ir_a_inicio(self):
        #devolverse al inicio
        self.mostrar(self.frame_inicio)

    def iniciar_partida(self):
        #iniciar la partida
        self.partida.reiniciar()
        self.frame_final.pack_forget()
        self.frame_respuestas.pack()
        self.actualizar_pregunta()
        self.mostrar(self.frame_juego)

    def actualizar_pregunta(self):
        self.label_pregunta.config(text=self.partida.texto_actual())

    def responder(self, es_si):
        # E: es_si (bool)
        # S: ninguna
        # Si está en una hoja, la respuesta confirma o rechaza la adivinanza;
        # si no, avanza por el árbol.
        if self.partida.es_hoja():
            if es_si:
                self.mostrar_resultado("¡Adiviné! Gané esta partida.")
            else:
                self.abrir_aprendizaje()
        else:
            self.partida.responder(es_si)
            self.actualizar_pregunta()

    def mostrar_resultado(self, mensaje):
        # E: mensaje (str)
        # S: ninguna

        self.label_pregunta.config(text=mensaje)
        self.frame_respuestas.pack_forget()
        self.frame_final.pack()
        self.mostrar(self.frame_juego)

    def abrir_aprendizaje(self):

        self.entrada_respuesta.delete(0, tk.END)
        self.entrada_pregunta.delete(0, tk.END)
        self.var_es_si.set("")
        self.label_diferenciar.config(
            text="Escribe una pregunta que diferencie tu respuesta de "
                 + self.partida.actual.texto + ":")
        self.mostrar(self.frame_aprender)

    def guardar_aprendizaje(self):
        # Valida los campos, le pide a la partida que aprenda y guarda el archivo
        respuesta = self.entrada_respuesta.get().strip()
        pregunta = self.entrada_pregunta.get().strip()
        eleccion = self.var_es_si.get()

        if respuesta == "":
            messagebox.showwarning("Dato faltante", "Escribe en qué estabas pensando.")
            return
        if pregunta == "":
            messagebox.showwarning("Dato faltante", "Escribe una pregunta que diferencie las respuestas.")
            return
        if eleccion == "":
            messagebox.showwarning("Dato faltante", "Indica si para tu respuesta la contestación es Sí o No.")
            return

        if not self.partida.aprender(respuesta, pregunta, eleccion == "si"):
            messagebox.showerror("Error", "No se pudo agregar la información al árbol.")
            return

        guardado, mensaje = self.gestor.guardar(self.arbol, self.ruta)
        if not guardado:
            messagebox.showwarning("Aviso", "Aprendí, pero no pude guardar el archivo.\n" + mensaje)
        self.mostrar_resultado("¡Gracias! Aprendí algo nuevo.")

    def cargar_archivo(self):
        # Si el archivo falla, avisa y se sigue con el árbol que ya había
        ruta = filedialog.askopenfilename(title="Cargar árbol",
                                          filetypes=[("Archivos de texto", "*.txt"),
                                                     ("Todos los archivos", "*.*")])
        if ruta == "":
            return

        arbol, mensaje = self.gestor.cargar(ruta)
        if arbol is None:
            messagebox.showerror("No se pudo cargar", mensaje + "\nSe continúa con el árbol actual.")
            return

        self.arbol = arbol
        self.partida = Partida(arbol)
        self.ruta = ruta
        self.label_estado.config(text="Árbol cargado de: " + ruta)
        messagebox.showinfo("Listo", mensaje)


if __name__ == "__main__":
    ventana = tk.Tk()
    Interfaz(ventana)
    ventana.mainloop()
