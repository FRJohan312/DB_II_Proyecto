import re
import tkinter as tk
from tkinter import messagebox, simpledialog, StringVar, OptionMenu
from servicios.usuario import registrar_usuario, verificar_credenciales
from gui.main_window import mostrar_ventana_principal
from estilos import (
    aplicar_estilos_ventana, crear_boton, crear_entry,
    crear_label, COLOR_ROJO, COLOR_FONDO
)

def es_correo_valido(correo):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, correo)

def mostrar_ventana_login():
    try:
        ventana = tk.Tk()
        aplicar_estilos_ventana(ventana, "Ingresar")
        ventana.geometry("420x300")

        # Etiqueta y campo de entrada para el correo
        crear_label(ventana, "Correo electrónico:").pack(pady=(20, 5))
        entrada_correo = crear_entry(ventana)
        entrada_correo.pack()

        # Función para iniciar sesión
        def login():
            try:
                correo = entrada_correo.get().strip()
                if not correo:
                    messagebox.showerror("Error", "Debe ingresar el correo.", parent=ventana)
                    return

                contraseña = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show='*', parent=ventana)
                if not contraseña:
                    messagebox.showerror("Error", "Debe ingresar la contraseña.", parent=ventana)
                    return

                usuario = verificar_credenciales(correo, contraseña)
                if usuario:
                    ventana.destroy()
                    mostrar_ventana_principal(usuario)
                else:
                    messagebox.showerror("Error", "Correo o contraseña inválidos.", parent=ventana)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema durante el login:\n{e}", parent=ventana)

        # Función para registrar nuevo usuario
        def registrar():
            try:
                correo = entrada_correo.get().strip()
                if not correo:
                    messagebox.showerror("Error", "Debe ingresar un correo.", parent=ventana)
                    return

                if not es_correo_valido(correo):
                    messagebox.showerror("Error", "Formato de correo inválido.", parent=ventana)
                    return

                nombre = simpledialog.askstring("Registro", "Nombre completo:", parent=ventana)
                if not nombre:
                    messagebox.showerror("Error", "Debe ingresar el nombre.", parent=ventana)
                    return

                contraseña = simpledialog.askstring("Registro", "Contraseña (mínimo 8 caracteres):", show="*", parent=ventana)
                if not contraseña or len(contraseña) < 8:
                    messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres.", parent=ventana)
                    return

                preferencias_raw = simpledialog.askstring("Preferencias", "Géneros preferidos (separados por comas):", parent=ventana)
                preferencias = [p.strip() for p in preferencias_raw.split(",")] if preferencias_raw else []

                # Ventana emergente para seleccionar el rol
                rol_ventana = tk.Toplevel(ventana)
                aplicar_estilos_ventana(rol_ventana, "Seleccione el Rol")
                rol_ventana.geometry("300x150")

                crear_label(rol_ventana, "Seleccione el rol:").pack(pady=10)
                rol_var = StringVar(rol_ventana)
                rol_var.set("usuario")

                menu = OptionMenu(rol_ventana, rol_var, "usuario", "admin")
                menu.config(font=("Segoe UI", 10), bg="white", width=15)
                menu.pack(pady=5)

                def confirmar_rol():
                    try:
                        rol = rol_var.get()
                        rol_ventana.destroy()

                        resultado = registrar_usuario(nombre, correo, contraseña, preferencias, rol)
                        if resultado:
                            messagebox.showinfo("Éxito", "Usuario registrado correctamente.", parent=ventana)
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
                            messagebox.showerror("Error", "No se pudo registrar el usuario.", parent=ventana)
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al confirmar el rol:\n{e}", parent=ventana)

                crear_boton(rol_ventana, "Confirmar", confirmar_rol).pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al registrar:\n{e}", parent=ventana)

        # Botones principales
        crear_boton(ventana, "Ingresar", login).pack(pady=10)
        crear_boton(ventana, "Registrarse", registrar).pack(pady=10)
        crear_boton(ventana, "Salir", ventana.destroy, color=COLOR_ROJO).pack(pady=20)

        ventana.mainloop()

    except Exception as e:
        messagebox.showerror("Error Crítico", f"No se pudo iniciar la ventana de login:\n{e}")
