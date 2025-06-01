import tkinter as tk
from tkinter import ttk, messagebox
from servicios.usuario import obtener_historial
from estilos import *

class VentanaHistorialCompras(tk.Toplevel):
    def __init__(self, master, usuario_id):
        super().__init__(master)
        aplicar_estilos_ventana(self, "Historial de Compras")
        self.geometry("600x400")
        self.usuario_id = usuario_id

        # Título
        crear_label(self, "Historial de Compras", font=FUENTE_TITULO).pack(pady=(10, 0))

        # Frame para envolver el Treeview y Scrollbar
        frame_tabla = tk.Frame(self, bg=COLOR_FONDO)
        frame_tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Treeview para mostrar el historial
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("pelicula", "funcion", "cantidad", "fecha"),
            show='headings',
            style="Estilo.Treeview"
        )

        # Encabezados
        self.tree.heading("pelicula", text="Película")
        self.tree.heading("funcion", text="Función")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("fecha", text="Fecha")

        # Ajuste de columnas
        for col in ("pelicula", "funcion", "cantidad", "fecha"):
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")

        # Scrollbar vertical
        scrollbar = crear_scrollbar(frame_tabla, "vertical")
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.estilizar_treeview()
        self.cargar_historial()

    def estilizar_treeview(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")  # Puedes cambiar a 'default' si no se ve bien
        estilo.configure(
            "Estilo.Treeview",
            background=COLOR_FONDO,
            foreground=COLOR_TEXTO,
            rowheight=25,
            fieldbackground=COLOR_FONDO,
            font=FUENTE
        )
        estilo.map("Estilo.Treeview", background=[("selected", COLOR_PRIMARIO)])

        estilo.configure(
            "Estilo.Treeview.Heading",
            background=COLOR_PRIMARIO,
            foreground="white",
            font=FUENTE_TITULO
        )

    def cargar_historial(self):
        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)

        historial = obtener_historial(self.usuario_id)

        if not historial:
            messagebox.showinfo("Sin compras", "Este usuario no tiene historial de compras.", parent=self)
            return

        # Insertar datos
        for compra in historial:
            self.tree.insert("", "end", values=(
                compra.get("pelicula", "N/A"),
                compra.get("funcion", "N/A"),
                compra.get("cantidad", "N/A"),
                compra.get("fecha", "N/A")
            ))
