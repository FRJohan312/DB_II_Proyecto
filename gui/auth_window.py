import tkinter as tk
from tkinter import messagebox, simpledialog
from models.usuario import registrar_usuario, obtener_usuario_por_correo
from gui.main_window import mostrar_ventana_principal

def mostrar_ventana_autenticacion():
    ventana = tk.Tk()
    ventana.title("Inicio - Cine")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Correo Electrónico:").pack(pady=5)
    entrada_correo = tk.Entry(ventana, width=40)
    entrada_correo.pack()

    def login():
        correo = entrada_correo.get().strip()
        usuario = obtener_usuario_por_correo(correo)
        if usuario:
            ventana.destroy()
            mostrar_ventana_principal(usuario)
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

    def registro():
        nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        if not nombre:
            return

        preferencias = simpledialog.askstring("Preferencias", "Géneros favoritos (separados por coma):")
        if preferencias:
            preferencias = [p.strip() for p in preferencias.split(",")]
        else:
            preferencias = []

        rol = simpledialog.askstring("Rol", "¿Administrador o Usuario? (Escribe 'admin' o 'usuario')").strip().lower()
        if rol not in ["admin", "usuario"]:
            messagebox.showerror("Error", "Rol inválido.")
            return

        resultado = registrar_usuario(nombre, entrada_correo.get().strip(), preferencias, rol)
        if resultado:
            messagebox.showinfo("Éxito", "Usuario registrado con éxito")
            ventana.destroy()
            mostrar_ventana_principal({
                "_id": resultado,
                "nombre": nombre,
                "correo": entrada_correo.get().strip(),
                "preferencias": preferencias,
                "rol": rol
            })
        else:
            messagebox.showerror("Error", "Error al registrar usuario")

    tk.Button(ventana, text="Ingresar", command=login).pack(pady=10)
    tk.Button(ventana, text="Registrarse", command=registro).pack(pady=10)

    ventana.mainloop()
