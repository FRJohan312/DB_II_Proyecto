import tkinter as tk
from tkinter import messagebox
from models.usuario import registrar_usuario
from gui.gestionar_peliculas import ventana_gestion_peliculas
from gui.comprar_entradas import VentanaCompraEntradas
from gui.historial_compras import VentanaHistorialCompras

def mostrar_ventana_principal():
    ventana = tk.Tk()
    ventana.title("Registro de Usuario - Cine")
    ventana.geometry("400x300")

    # Etiquetas y entradas
    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana, width=40)
    entrada_nombre.pack()

    tk.Label(ventana, text="Correo electrónico:").pack(pady=5)
    entrada_correo = tk.Entry(ventana, width=40)
    entrada_correo.pack()

    tk.Label(ventana, text="Preferencias (separadas por comas):").pack(pady=5)
    entrada_preferencias = tk.Entry(ventana, width=40)
    entrada_preferencias.pack()

    def mostrar_historial(usuario_id):
        ventana = VentanaHistorialCompras(None, usuario_id)
        ventana.grab_set()  # Para que sea modal

    def registrar():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        preferencias = [p.strip() for p in entrada_preferencias.get().split(",") if p.strip()]

        if not nombre or not correo:
            messagebox.showerror("Error", "Nombre y correo son obligatorios.")
            return

        resultado = registrar_usuario(nombre, correo, preferencias)
        messagebox.showinfo("Resultado", resultado)
        if resultado:
            messagebox.showinfo("Éxito", "Usuario registrado con éxito")

            usuario = {
            "_id": resultado,
            "nombre": nombre,
            "correo": correo,
            "preferencias": preferencias
        }
            btn_historial = tk.Button(ventana, text="Ver Historial de Compras", command=lambda: VentanaHistorialCompras(ventana, usuario["_id"]))
            btn_historial.pack(pady=10)
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario")
    
    btn_gestion_peliculas = tk.Button(ventana, text="Gestionar Películas", command=ventana_gestion_peliculas)
    btn_gestion_peliculas.pack(pady=10)
    btn_comprar = tk.Button(ventana, text="Comprar Entradas", command=lambda: VentanaCompraEntradas())
    btn_comprar.pack(pady=10)



    

    # Botón de registro
    tk.Button(ventana, text="Registrar Usuario", command=registrar).pack(pady=15)
    
    ventana.mainloop()
