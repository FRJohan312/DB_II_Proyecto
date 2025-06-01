# estilos.py
import tkinter as tk

# Colores modernos y agradables
COLOR_FONDO = "#F4F6F8"
COLOR_PRIMARIO = "#4A90E2"
COLOR_SECUNDARIO = "#7B8D93"
COLOR_ROJO = "#E74C3C"
COLOR_VERDE = "#2ECC71"
FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE_NORMAL = ("Segoe UI", 11)

def aplicar_estilos_ventana(ventana, titulo=""):
    ventana.configure(bg=COLOR_FONDO)
    if titulo:
        ventana.title(titulo)

def crear_label(padre, texto):
    return tk.Label(padre, text=texto, bg=COLOR_FONDO, fg="#333", font=FUENTE_NORMAL)

def crear_entry(padre):
    return tk.Entry(padre, font=FUENTE_NORMAL, relief="solid", bd=1)

def crear_boton(padre, texto, comando, color=COLOR_PRIMARIO):
    return tk.Button(
        padre, text=texto, command=comando,
        bg=color, fg="white", activebackground="#3367D6",
        relief="flat", font=FUENTE_NORMAL, padx=10, pady=5
    )
