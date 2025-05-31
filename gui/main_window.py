import tkinter as tk
from tkinter import messagebox
from gui.gestionar_peliculas import ventana_gestion_peliculas
from gui.comprar_entradas import VentanaCompraEntradas
from gui.historial_compras import VentanaHistorialCompras
from gui.gestionar_usuarios import VentanaGestionUsuarios
from gui.navigation import volver_al_login

def mostrar_ventana_principal(usuario):
    try:
        # Validación de campos esenciales
        if not isinstance(usuario, dict) or not all(k in usuario for k in ("nombre", "rol", "_id")):
            raise ValueError("Datos de usuario incompletos o incorrectos.")

        ventana = tk.Tk()
        ventana.title("Panel Principal - Cine")
        ventana.geometry("400x300")

        tk.Label(ventana, text=f"Bienvenido, {usuario['nombre']} ({usuario['rol']})").pack(pady=10)

        if usuario["rol"] == "admin":
            tk.Button(ventana, text="Gestionar Películas", command=proteger_funcion(ventana_gestion_peliculas)).pack(pady=10)
            tk.Button(ventana, text="Gestionar Usuarios", command=proteger_funcion(VentanaGestionUsuarios)).pack(pady=10)

        tk.Button(ventana, text="Comprar Entradas",
                  command=proteger_funcion(lambda: VentanaCompraEntradas(usuario))).pack(pady=10)

        tk.Button(ventana, text="Ver Historial de Compras",
                  command=proteger_funcion(lambda: VentanaHistorialCompras(ventana, usuario["_id"]))).pack(pady=10)

        tk.Button(ventana, text="Cerrar Sesión", fg="white", bg="red",
                  command=lambda: volver_al_login(ventana)).pack(pady=20)

        ventana.mainloop()

    except Exception as e:
        messagebox.showerror("Error crítico", f"Ocurrió un error al abrir el panel principal:\n{e}")

def proteger_funcion(func):
    """
    Decorador de funciones para envolver los callbacks y evitar que errores rompan el flujo principal.
    """
    def wrapper():
        try:
            func()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")
    return wrapper
