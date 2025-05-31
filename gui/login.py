from tkinter import Tk, Label, Entry, Button, messagebox, simpledialog
from models.usuario import registrar_usuario, verificar_credenciales
from gui.main_window import mostrar_ventana_principal

def mostrar_ventana_login():
    ventana = Tk()
    ventana.title("Login o Registro")
    ventana.geometry("400x250")

    Label(ventana, text="Correo electrónico:").pack(pady=5)
    entrada_correo = Entry(ventana, width=40)
    entrada_correo.pack()

    def login():
        correo = entrada_correo.get().strip()
        contraseña = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show='*')

        usuario = verificar_credenciales(correo, contraseña)
        if usuario:
            ventana.destroy()
            mostrar_ventana_principal(usuario)
        else:
            messagebox.showerror("Error", "Correo o contraseña inválidos.")

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

    Button(ventana, text="Ingresar", command=login).pack(pady=10)
    Button(ventana, text="Registrarse", command=registrar).pack(pady=10)
    Button(ventana, text="Salir", fg="white", bg="purple", command=ventana.destroy).pack(pady=20)

    ventana.mainloop()