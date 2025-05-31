import re
import tkinter as tk
from tkinter import messagebox, simpledialog, StringVar, OptionMenu
from models.usuario import registrar_usuario, verificar_credenciales
from gui.main_window import mostrar_ventana_principal

def es_correo_valido(correo):
    # Expresión regular simple para validar correos
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, correo)

def mostrar_ventana_login():
    try:
        ventana = tk.Tk()
        ventana.title("Ingresar")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Correo electrónico:").pack(pady=5)
        entrada_correo = tk.Entry(ventana, width=40)
        entrada_correo.pack()

        def login():
            try:
                correo = entrada_correo.get().strip()
                if not correo:
                    messagebox.showerror("Error", "Debe ingresar el correo.", parent=ventana)
                    return

                # if not es_correo_valido(correo):
                #     messagebox.showerror("Error", "Correo electrónico inválido.", parent=ventana)
                #     return

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

                # Ventana temporal para elegir rol con OptionMenu
                rol_ventana = tk.Toplevel(ventana)
                rol_ventana.title("Seleccione el Rol")
                tk.Label(rol_ventana, text="Seleccione el rol:").pack(pady=5)

                rol_var = StringVar(rol_ventana)
                rol_var.set("usuario")  # valor por defecto

                opciones_rol = ["usuario", "admin"]
                menu_roles = OptionMenu(rol_ventana, rol_var, *opciones_rol)
                menu_roles.pack(pady=10)

                def confirmar_rol():
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

                tk.Button(rol_ventana, text="Confirmar", command=confirmar_rol).pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al registrar:\n{e}", parent=ventana)

        tk.Button(ventana, text="Ingresar", command=login).pack(pady=10)
        tk.Button(ventana, text="Registrarse", command=registrar).pack(pady=10)
        tk.Button(ventana, text="Salir", fg="white", bg="purple", command=ventana.destroy).pack(pady=20)

        ventana.mainloop()
    except Exception as e:
        messagebox.showerror("Error Crítico", f"No se pudo iniciar la ventana de login:\n{e}")
