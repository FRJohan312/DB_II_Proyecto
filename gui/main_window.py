import tkinter as tk
from gui.gestionar_peliculas import ventana_gestion_peliculas
from gui.comprar_entradas import VentanaCompraEntradas
from gui.historial_compras import VentanaHistorialCompras
from gui.gestionar_usuarios import VentanaGestionUsuarios
from gui.navigation import volver_al_login

def mostrar_ventana_principal(usuario):
    ventana = tk.Tk()
    ventana.title("Panel Principal - Cine")
    ventana.geometry("400x300")

    tk.Label(ventana, text=f"Bienvenido, {usuario['nombre']} ({usuario['rol']})").pack(pady=10)

    if usuario["rol"] == "admin":
        tk.Button(ventana, text="Gestionar Películas", command=ventana_gestion_peliculas).pack(pady=10)
        tk.Button(ventana, text="Gestionar Usuarios", command=VentanaGestionUsuarios).pack(pady=10)

    tk.Button(ventana, text="Comprar Entradas", command=lambda: VentanaCompraEntradas(usuario)).pack(pady=10)
    tk.Button(ventana, text="Ver Historial de Compras", command=lambda: VentanaHistorialCompras(ventana, usuario["_id"])).pack(pady=10)
    tk.Button(ventana, text="Cerrar Sesión", fg="white", bg="red", command=lambda: volver_al_login(ventana)).pack(pady=20)

    ventana.mainloop()