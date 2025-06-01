import tkinter as tk
from tkinter import messagebox, simpledialog
from servicios.usuario import obtener_usuarios, registrar_usuario, actualizar_usuario, eliminar_usuario

class VentanaGestionUsuarios(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Usuarios")
        self.geometry("600x480")

        # Lista de usuarios y Listbox
        self.usuarios = []
        self.lista = tk.Listbox(self, width=80)
        self.lista.pack(pady=10)

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Crear", command=self.crear_usuario).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", command=self.editar_usuario).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_usuario).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Regresar", command=self.destroy).grid(row=0, column=3, padx=5)

        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        self.usuarios = obtener_usuarios()
        for u in self.usuarios:
            self.lista.insert(tk.END, f"{u['nombre']} | {u['correo']} | {u['rol']}")

    def crear_usuario(self):
        nombre = simpledialog.askstring("Nombre", "Nombre completo:", parent=self)
        correo = simpledialog.askstring("Correo", "Correo electrónico:", parent=self)
        contraseña = simpledialog.askstring("Contraseña", "Contraseña:", show="*", parent=self)
        preferencias = simpledialog.askstring("Preferencias", "Géneros preferidos (separados por comas):", parent=self)

        if not all([nombre, correo, contraseña]):
            messagebox.showerror("Error", "Nombre, correo y contraseña son obligatorios.", parent=self)
            return

        # Ventana para seleccionar rol
        self.seleccionar_rol(lambda rol: self.confirmar_creacion(nombre, correo, contraseña, preferencias, rol))

    def seleccionar_rol(self, callback):
        ventana_rol = tk.Toplevel(self)
        ventana_rol.title("Seleccionar Rol")

        tk.Label(ventana_rol, text="Seleccione el rol:").pack(pady=5)
        rol_var = tk.StringVar(ventana_rol)
        rol_var.set("usuario")

        opciones = ["admin", "usuario"]
        tk.OptionMenu(ventana_rol, rol_var, *opciones).pack(pady=5)

        def confirmar():
            rol = rol_var.get()
            ventana_rol.destroy()
            callback(rol)

        tk.Button(ventana_rol, text="Confirmar", command=confirmar).pack(pady=10)

    def confirmar_creacion(self, nombre, correo, contraseña, preferencias, rol):
        preferencias_lista = [p.strip() for p in preferencias.split(",")] if preferencias else []
        resultado = registrar_usuario(nombre, correo, contraseña, preferencias_lista, rol)

        if resultado:
            messagebox.showinfo("Éxito", "Usuario creado correctamente.", parent=self)
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.", parent=self)

    def editar_usuario(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario.", parent=self)
            return

        usuario = self.usuarios[seleccion[0]]

        nombre = simpledialog.askstring("Nombre", "Nombre completo:", initialvalue=usuario["nombre"], parent=self)
        preferencias = simpledialog.askstring("Preferencias", "Géneros preferidos:", initialvalue=", ".join(usuario["preferencias"]), parent=self)
        rol = simpledialog.askstring("Rol", "Rol:", initialvalue=usuario["rol"], parent=self)

        if not all([nombre, rol]):
            messagebox.showerror("Error", "Nombre y rol son obligatorios.", parent=self)
            return

        preferencias_lista = [p.strip() for p in preferencias.split(",")] if preferencias else []
        actualizado = actualizar_usuario(usuario["_id"], nombre, preferencias_lista, rol)

        if actualizado:
            messagebox.showinfo("Éxito", "Usuario actualizado.", parent=self)
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario.", parent=self)

    def eliminar_usuario(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario.", parent=self)
            return

        usuario = self.usuarios[seleccion[0]]
        confirmacion = messagebox.askyesno("Eliminar", f"¿Eliminar al usuario {usuario['correo']}?", parent=self)

        if confirmacion:
            eliminado = eliminar_usuario(usuario["_id"])
            if eliminado:
                messagebox.showinfo("Éxito", "Usuario eliminado.", parent=self)
                self.actualizar_lista()
            else:
                messagebox.showerror("Error", "No se pudo eliminar al usuario.", parent=self)
