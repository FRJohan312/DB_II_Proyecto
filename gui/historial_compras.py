import tkinter as tk
from tkinter import ttk, messagebox
from servicios.usuario import obtener_historial

class VentanaHistorialCompras(tk.Toplevel):
    def __init__(self, master, usuario_id):
        super().__init__(master)
        self.title("Historial de Compras")
        self.geometry("600x400")
        self.usuario_id = usuario_id

        # Árbol para mostrar historial
        self.tree = ttk.Treeview(
            self, columns=("pelicula", "funcion", "cantidad", "fecha"), show='headings'
        )

        # Encabezados del árbol
        self.tree.heading("pelicula", text="Película")
        self.tree.heading("funcion", text="Función")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("fecha", text="Fecha")

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        self.cargar_historial()

    def cargar_historial(self):
        # Limpia el árbol antes de insertar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        historial = obtener_historial(self.usuario_id)

        if not historial:
            messagebox.showinfo("Sin compras", "Este usuario no tiene historial de compras.", parent=self)
            return

        # Insertar cada compra en el árbol
        for compra in historial:
            self.tree.insert("", "end", values=(
                compra.get("pelicula", "N/A"),
                compra.get("funcion", "N/A"),
                compra.get("cantidad", "N/A"),
                compra.get("fecha", "N/A")
            ))
