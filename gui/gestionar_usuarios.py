import tkinter as tk
from tkinter import messagebox, simpledialog
from servicios.usuario import obtener_usuarios, registrar_usuario, actualizar_usuario, eliminar_usuario
from estilos import *

class VentanaGestionUsuarios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        aplicar_estilos_ventana(self, "Gestión de Usuarios")
        self.geometry("600x480")

        self.usuarios = []

        # Listbox con scrollbar
        frame_lista = tk.Frame(self, bg=COLOR_FONDO)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(frame_lista)
        self.scrollbar.pack(side="right", fill="y")

        self.lista = tk.Listbox(frame_lista, width=80, yscrollcommand=self.scrollbar.set, font=FUENTE)
        self.lista.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.lista.yview)

        # Botones
        btn_frame = tk.Frame(self, bg=COLOR_FONDO)
        btn_frame.pack(pady=10)

        btn_crear = crear_boton(btn_frame, "Crear", self.crear_usuario)
        btn_crear.grid(row=0, column=0, padx=5)

        btn_editar = crear_boton(btn_frame, "Editar", self.editar_usuario)
        btn_editar.grid(row=0, column=1, padx=5)

        btn_eliminar = crear_boton(btn_frame, "Eliminar", self.eliminar_usuario, color=COLOR_ROJO)
        btn_eliminar.grid(row=0, column=2, padx=5)

        btn_regresar = crear_boton(btn_frame, "Regresar", self.destroy, color=COLOR_ROJO)
        btn_regresar.grid(row=0, column=3, padx=5)

        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        self.usuarios = obtener_usuarios()
        for u in self.usuarios:
            texto = f"{u['nombre']} | {u['correo']} | {u['rol']}"
            self.lista.insert(tk.END, texto)

    def crear_usuario(self):
        nombre = simpledialog.askstring("Nombre", "Nombre completo:", parent=self)
        correo = simpledialog.askstring("Correo", "Correo electrónico:", parent=self)
        contraseña = simpledialog.askstring("Contraseña", "Contraseña:", show="*", parent=self)
        preferencias = simpledialog.askstring("Preferencias", "Géneros preferidos (separados por comas):", parent=self)

        if not all([nombre, correo, contraseña]):
            messagebox.showerror("Error", "Nombre, correo y contraseña son obligatorios.", parent=self)
            return

        self.seleccionar_rol(lambda rol: self.confirmar_creacion(nombre, correo, contraseña, preferencias, rol))

    def seleccionar_rol(self, callback):
        ventana_rol = tk.Toplevel(self)
        aplicar_estilos_ventana(ventana_rol, "Seleccionar Rol")
        ventana_rol.geometry("250x150")

        crear_label(ventana_rol, "Seleccione el rol:").pack(pady=10)
        rol_var = tk.StringVar(ventana_rol)
        rol_var.set("usuario")

        opciones = ["admin", "usuario"]
        opcion_menu = tk.OptionMenu(ventana_rol, rol_var, *opciones)
        opcion_menu.pack(pady=10)

        btn_confirmar = crear_boton(ventana_rol, "Confirmar", lambda: (ventana_rol.destroy(), callback(rol_var.get())))
        btn_confirmar.pack(pady=10)

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

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.", parent=self)
            return

        # Ventana para seleccionar nuevo rol
        ventana_rol = tk.Toplevel(self)
        aplicar_estilos_ventana(ventana_rol, "Seleccionar Rol")
        ventana_rol.geometry("250x150")

        crear_label(ventana_rol, "Seleccione el nuevo rol:").pack(pady=10)
        rol_var = tk.StringVar(ventana_rol)
        rol_var.set(usuario["rol"])  # valor inicial

        opciones = ["admin", "usuario"]
        opcion_menu = tk.OptionMenu(ventana_rol, rol_var, *opciones)
        opcion_menu.config(font=COLOR_TEXTO)
        opcion_menu.pack(pady=10)

        def confirmar():
            rol = rol_var.get()
            preferencias_lista = [p.strip() for p in preferencias.split(",")] if preferencias else []
            actualizado = actualizar_usuario(usuario["_id"], nombre, preferencias_lista, rol)

            if actualizado:
                messagebox.showinfo("Éxito", "Usuario actualizado.", parent=self)
                self.actualizar_lista()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario.", parent=self)

            ventana_rol.destroy()

        crear_boton(ventana_rol, "Confirmar", confirmar).pack(pady=10)

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
