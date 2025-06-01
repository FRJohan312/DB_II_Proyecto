import tkinter as tk
from tkinter import messagebox
from gui.gestionar_peliculas import ventana_gestion_peliculas
from gui.comprar_entradas import VentanaCompraEntradas
from gui.historial_compras import VentanaHistorialCompras
from gui.gestionar_usuarios import VentanaGestionUsuarios
from gui.navigation import volver_al_login

def mostrar_ventana_principal(usuario):
    try:
        if not isinstance(usuario, dict) or not all(k in usuario for k in ("nombre", "rol", "_id")):
            raise ValueError("Datos de usuario incompletos o incorrectos.")

        ventana = tk.Tk()
        ventana.title("Panel Principal")
        ventana.geometry("450x400")
        ventana.configure(bg="#f0f4f8")  # Fondo claro

        # Estilo global
        fuente_titulo = ("Helvetica", 16, "bold")
        fuente_boton = ("Helvetica", 12)
        color_boton = "#4a90e2"
        color_texto_boton = "white"

        # Frame principal
        frame = tk.Frame(ventana, bg="#f0f4f8")
        frame.pack(expand=True)

        # Bienvenida
        bienvenida = tk.Label(
            frame, 
            text=f"Bienvenido, {usuario['nombre']} ({usuario['rol']})",
            font=fuente_titulo, bg="#f0f4f8", fg="#333"
        )
        bienvenida.pack(pady=20)

        def crear_boton(texto, comando, color=color_boton):
            return tk.Button(
                frame, text=texto, font=fuente_boton, width=25, height=2,
                bg=color, fg=color_texto_boton, bd=0, activebackground="#357ABD",
                command=proteger_funcion(comando)
            )

        # Opciones para administrador
        if usuario["rol"] == "admin":
            crear_boton("🎞 Gestionar Películas", ventana_gestion_peliculas).pack(pady=5)
            crear_boton("👥 Gestionar Usuarios", lambda: VentanaGestionUsuarios(ventana)).pack(pady=5)

        # Opciones comunes
        crear_boton("🎟 Comprar Entradas", lambda: VentanaCompraEntradas(usuario)).pack(pady=5)
        crear_boton("📜 Ver Historial de Compras", lambda: VentanaHistorialCompras(ventana, usuario["_id"])).pack(pady=5)

        # Botón cerrar sesión
        tk.Button(
            frame, text="⛔ Cerrar Sesión", font=fuente_boton, width=25, height=2,
            bg="#e74c3c", fg="white", bd=0, activebackground="#c0392b",
            command=lambda: volver_al_login(ventana)
        ).pack(pady=20)

        ventana.mainloop()

    except Exception as e:
        messagebox.showerror("Error crítico", f"Ocurrió un error al abrir el panel principal:\n{e}")

def proteger_funcion(func):
    def wrapper():
        try:
            func()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")
    return wrapper
