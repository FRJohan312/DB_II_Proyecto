import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from models.usuario import obtener_usuarios, registrar_usuario, actualizar_usuario, eliminar_usuario

class VentanaGestionUsuarios(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Usuarios")
        self.geometry("600x400")

        self.usuarios = obtener_usuarios()

        self.lista = tk.Listbox(self, width=80)
        self.lista.pack(pady=10)
        self.actualizar_lista()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Crear", command=self.crear_usuario).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", command=self.editar_usuario).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_usuario).grid(row=0, column=2, padx=5)

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        self.usuarios = obtener_usuarios()
        for u in self.usuarios:
            self.lista.insert(tk.END, f"{u['nombre']} | {u['correo']} | {u['rol']}")

    def crear_usuario(self):
        nombre = simpledialog.askstring("Nombre", "Nombre completo:")
        correo = simpledialog.askstring("Correo", "Correo electrónico:")
        contraseña = simpledialog.askstring("Contraseña", "Contraseña:", show="*")
        preferencias = simpledialog.askstring("Preferencias", "Géneros preferidos (separados por comas):")
        rol = simpledialog.askstring("Rol", "Rol (admin o usuario):")

        if not all([nombre, correo, contraseña, rol]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        preferencias_lista = [p.strip() for p in preferencias.split(",")] if preferencias else []
        resultado = registrar_usuario(nombre, correo, contraseña, preferencias_lista, rol)
        if resultado:
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            self.actualizar_lista()

    def editar_usuario(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario.")
            return

        usuario = self.usuarios[seleccion[0]]

        nombre = simpledialog.askstring("Nombre", "Nombre completo:", initialvalue=usuario["nombre"])
        preferencias = simpledialog.askstring("Preferencias", "Géneros preferidos:", initialvalue=", ".join(usuario["preferencias"]))
        rol = simpledialog.askstring("Rol", "Rol:", initialvalue=usuario["rol"])

        if not all([nombre, rol]):
            messagebox.showerror("Error", "Nombre y rol son obligatorios.")
            return

        preferencias_lista = [p.strip() for p in preferencias.split(",")] if preferencias else []
        actualizado = actualizar_usuario(usuario["_id"], nombre, preferencias_lista, rol)
        if actualizado:
            messagebox.showinfo("Éxito", "Usuario actualizado.")
            self.actualizar_lista()

    def eliminar_usuario(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario.")
            return

        usuario = self.usuarios[seleccion[0]]
        confirmacion = messagebox.askyesno("Eliminar", f"¿Eliminar al usuario {usuario['correo']}?")
        if confirmacion:
            eliminar_usuario(usuario["_id"])
            self.actualizar_lista()
