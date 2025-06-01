import tkinter as tk

# Colores modernos y agradables
COLOR_FONDO = "#F4F6F8"
COLOR_PRIMARIO = "#4A90E2"
COLOR_SECUNDARIO = "#7B8D93"
COLOR_ROJO = "#E74C3C"
COLOR_VERDE = "#2ECC71"
COLOR_TEXTO = "#333333"
COLOR_ACTIVO = "#3367D6"

# Fuentes
FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE = ("Segoe UI", 11)  # Fuente normal para todo

def aplicar_estilos_ventana(ventana, titulo=""):
    ventana.configure(bg=COLOR_FONDO)
    if titulo:
        ventana.title(titulo)

def crear_label(padre, texto, fg=COLOR_TEXTO, font=FUENTE):
    return tk.Label(padre, text=texto, bg=COLOR_FONDO, fg=fg, font=font)

def crear_entry(padre):
    return tk.Entry(padre, font=FUENTE, relief="solid", bd=1)

def crear_boton(padre, texto, comando, color=COLOR_PRIMARIO, fg="white"):
    return tk.Button(
        padre, text=texto, command=comando,
        bg=color, fg=fg, activebackground=COLOR_ACTIVO,
        relief="flat", font=FUENTE, padx=10, pady=5,
        cursor="hand2"
    )

def crear_scrollbar(padre, orientacion="vertical"):
    sb = tk.Scrollbar(padre, orient=orientacion)
    # No todos los sistemas permiten estilos, pero podemos intentar bg/active
    sb.config(bg=COLOR_SECUNDARIO, troughcolor=COLOR_FONDO, relief="flat", borderwidth=0)
    return sb

def crear_optionmenu(padre, variable, opciones, font=FUENTE, bg=COLOR_FONDO, fg=COLOR_TEXTO):
    opcion_menu = tk.OptionMenu(padre, variable, *opciones)
    opcion_menu.config(font=font, bg=bg, fg=fg, activebackground=COLOR_PRIMARIO, activeforeground="white")
    menu = opcion_menu["menu"]
    menu.config(font=font, bg=bg, fg=fg)
    return opcion_menu

