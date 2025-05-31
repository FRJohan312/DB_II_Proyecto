import tkinter as tk
from tkinter import messagebox, simpledialog
from models.usuario import registrar_usuario, obtener_usuario_por_correo, verificar_credenciales
from gui.gestionar_peliculas import ventana_gestion_peliculas
from gui.comprar_entradas import VentanaCompraEntradas
from gui.historial_compras import VentanaHistorialCompras

# Ventana Principal (según rol)
def mostrar_ventana_principal(usuario):
    ventana = tk.Tk()
    ventana.title("Panel Principal - Cine")
    ventana.geometry("400x300")

    tk.Label(ventana, text=f"Bienvenido, {usuario['nombre']} ({usuario['rol']})").pack(pady=10)

    if usuario["rol"] == "admin":
        tk.Button(ventana, text="Gestionar Películas", command=ventana_gestion_peliculas).pack(pady=10)

    tk.Button(ventana, text="Comprar Entradas", command=lambda: VentanaCompraEntradas(usuario)).pack(pady=10)
    tk.Button(ventana, text="Ver Historial de Compras", command=lambda: VentanaHistorialCompras(ventana, usuario["_id"])).pack(pady=10)

    tk.Button(ventana, text="Cerrar Sesión", fg="white", bg="red", command=lambda: cerrar_sesion(ventana)).pack(pady=20)

    ventana.mainloop()

def cerrar_sesion(ventana_actual):
    ventana_actual.destroy()
    mostrar_ventana_login()

def salir(ventana_actual):
    ventana_actual.destroy()

# Ventana de Login y Registro
def mostrar_ventana_login():
    ventana = tk.Tk()
    ventana.title("Login o Registro - Cine")
    ventana.geometry("400x250")

    tk.Label(ventana, text="Correo electrónico:").pack(pady=5)
    entrada_correo = tk.Entry(ventana, width=40)
    entrada_correo.pack()

    tk.Button(ventana, text="Salir", fg="white", bg="red", command=lambda: salir(ventana)).pack(pady=20)

    def login():
        correo = entrada_correo.get().strip()
        contraseña = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show='*')

        usuario = verificar_credenciales(correo, contraseña)
        if usuario:
            ventana.destroy()
            mostrar_ventana_principal(usuario)
        else:
            messagebox.showerror("Error", "Correo o contraseña invalidos.")

    def registrar():
        correo = entrada_correo.get().strip()
        if not correo:
            messagebox.showerror("Error", "Debe ingresar un correo.")
            return

        nombre = simpledialog.askstring("Registro", "Nombre completo:")
        if not nombre:
            return

        contraseña = simpledialog.askstring("Registro", "Contraseña:", show="*")
        if not contraseña:
            return

        preferencias_raw = simpledialog.askstring("Preferencias", "Géneros preferidos (separados por comas):")
        preferencias = [p.strip() for p in preferencias_raw.split(",")] if preferencias_raw else []

        rol = simpledialog.askstring("Rol", "¿Rol del usuario? (admin o usuario):")
        if rol not in ["admin", "usuario"]:
            messagebox.showerror("Error", "Rol inválido.")
            return

        resultado = registrar_usuario(nombre, correo, contraseña, preferencias, rol)
        if resultado:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            usuario = {
                "_id": resultado,
                "nombre": nombre,
                "correo": correo,
                "preferencias": preferencias,
                "rol": rol
            }
            ventana.destroy()
            mostrar_ventana_principal(usuario)
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.")


    tk.Button(ventana, text="Ingresar", command=login).pack(pady=10)
    tk.Button(ventana, text="Registrarse", command=registrar).pack(pady=10)

    ventana.mainloop()
