import tkinter as tk
from tkinter import ttk
from models.usuario import obtener_historial

class VentanaHistorialCompras(tk.Toplevel):
    def __init__(self, master, usuario_id):
        super().__init__(master)
        self.title("Historial de Compras")
        self.geometry("600x400")

        self.usuario_id = usuario_id

        self.tree = ttk.Treeview(self, columns=("pelicula", "funcion", "cantidad", "fecha"), show='headings')
        self.tree.heading("pelicula", text="Película")
        self.tree.heading("funcion", text="Función")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("fecha", text="Fecha")

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        self.cargar_historial()

    def cargar_historial(self):
        historial = obtener_historial(self.usuario_id)
        for compra in historial:
            self.tree.insert("", "end", values=(
                compra.get("pelicula", ""),
                compra.get("funcion", ""),
                compra.get("cantidad", ""),
                compra.get("fecha", "")
            ))
    
