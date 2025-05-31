import tkinter as tk
from tkinter import messagebox, ttk
from models.usuario import obtener_usuarios
from models.pelicula import obtener_peliculas
from models.entrada import comprar_entrada, obtener_historial_usuario
from datetime import datetime

class VentanaCompraEntradas(tk.Toplevel):
    def __init__(self, usuario_logeado):
        super().__init__()
        self.title("Compra de Entradas")
        self.usuario_logeado = usuario_logeado

        # Obtener usuarios y películas
        self.usuarios = obtener_usuarios()
        self.peliculas = obtener_peliculas()

        self.label_disponibilidad = tk.Label(self, text="Disponibilidad: N/A")
        self.label_disponibilidad.grid(row=3, column=2, padx=10)

        if self.usuario_logeado["rol"] == "admin":
            tk.Label(self, text="Usuario:").grid(row=0, column=0)
            self.usuario_combo = ttk.Combobox(self, values=[u["correo"] for u in self.usuarios])
            self.usuario_combo.grid(row=0, column=1)
        else:
            tk.Label(self, text="Usuario:").grid(row=0, column=0)
            tk.Label(self, text=self.usuario_logeado["correo"], fg="gray").grid(row=0, column=1)

        tk.Label(self, text="Película:").grid(row=1, column=0)
        self.pelicula_combo = ttk.Combobox(self, values=[p["nombre"] for p in self.peliculas])
        self.pelicula_combo.grid(row=1, column=1)
        self.pelicula_combo.bind("<<ComboboxSelected>>", self.cargar_funciones)

        tk.Label(self, text="Función (hora):").grid(row=2, column=0)
        self.funcion_combo = ttk.Combobox(self, values=[])
        self.funcion_combo.grid(row=2, column=1)
        self.funcion_combo.bind("<<ComboboxSelected>>", self.actualizar_disponibilidad)

        tk.Label(self, text="Cantidad:").grid(row=3, column=0)
        self.entry_cantidad = tk.Entry(self)
        self.entry_cantidad.grid(row=3, column=1)
        self.entry_cantidad.insert(0, "1")

        btn_comprar = tk.Button(self, text="Comprar", command=self.realizar_compra)
        btn_comprar.grid(row=4, column=0, columnspan=2, pady=10)

        self.recibo_text = tk.Text(self, height=10, width=50)
        self.recibo_text.grid(row=5, column=0, columnspan=2)

    def cargar_funciones(self, event=None):
        pelicula_nombre = self.pelicula_combo.get()
        self.funcion_combo.set('')
        self.funcion_combo['values'] = []
        self.label_disponibilidad.config(text="Disponibilidad: N/A")

        pelicula = next((p for p in self.peliculas if p["nombre"] == pelicula_nombre), None)
        if pelicula:
            horas = [f["hora"] + f" (Disp: {f['disponibles']})" for f in pelicula["funciones"]]
            self.funcion_combo['values'] = horas


    def realizar_compra(self):
        if self.usuario_logeado["rol"] == "admin":
            correo_usuario = self.usuario_combo.get()
            usuario = next((u for u in self.usuarios if u["correo"] == correo_usuario), None)
        else:
            usuario = self.usuario_logeado
            correo_usuario = usuario["correo"]

        pelicula_nombre = self.pelicula_combo.get()
        funcion_hora = self.funcion_combo.get()
        cantidad_str = self.entry_cantidad.get()

        if not correo_usuario or not pelicula_nombre or not funcion_hora or not cantidad_str:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        pelicula = next((p for p in self.peliculas if p["nombre"] == pelicula_nombre), None)

        if not usuario or not pelicula:
            messagebox.showerror("Error", "Usuario o película no encontrados")
            return

        # Función sin disponibilidad entre paréntesis
        hora_real = funcion_hora.split(" ")[0]

        exito, mensaje = comprar_entrada(str(usuario["_id"]), str(pelicula["_id"]), hora_real, cantidad)
        if exito:
            self.mostrar_recibo(usuario, pelicula, hora_real, cantidad, mensaje)
            # Recargar película para obtener funciones actualizadas (desde la BD)
            self.peliculas = obtener_peliculas()
            self.cargar_funciones()
            # Volver a seleccionar la función comprada para refrescar disponibilidad
            self.funcion_combo.set(funcion_hora)
            self.actualizar_disponibilidad()
        else:
            messagebox.showerror("Error", mensaje)

    def mostrar_recibo(self, usuario, pelicula, hora, cantidad, mensaje):
        self.recibo_text.delete("1.0", tk.END)
        texto = (
            f"RECIBO DE COMPRA\n"
            f"Usuario: {usuario['nombre']} ({usuario['correo']})\n"
            f"Película: {pelicula['nombre']}\n"
            f"Función: {hora}\n"
            f"Cantidad: {cantidad}\n"
            f"Mensaje: {mensaje}\n"
            f"Gracias por su compra!"
        )
        self.recibo_text.insert(tk.END, texto)

    def actualizar_disponibilidad(self, event=None):
        funcion_hora = self.funcion_combo.get()
        if not funcion_hora:
            self.label_disponibilidad.config(text="Disponibilidad: N/A")
            return

        pelicula_nombre = self.pelicula_combo.get()
        pelicula = next((p for p in self.peliculas if p["nombre"] == pelicula_nombre), None)
        if not pelicula:
            self.label_disponibilidad.config(text="Disponibilidad: N/A")
            return

        hora_real = funcion_hora.split(" ")[0]
        funcion = next((f for f in pelicula["funciones"] if f["hora"] == hora_real), None)
        if funcion:
            disponibles = funcion["disponibles"]
            self.label_disponibilidad.config(text=f"Disponibilidad: {disponibles}")
        else:
            self.label_disponibilidad.config(text="Disponibilidad: N/A")