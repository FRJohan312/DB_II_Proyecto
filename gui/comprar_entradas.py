import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from models.usuario import obtener_usuarios
from models.pelicula import obtener_peliculas
from models.entrada import comprar_entrada
from db import get_db

PRECIO_ENTRADA = 9000  # Precio fijo por entrada

class VentanaCompraEntradas(tk.Toplevel):
    def __init__(self, usuario_logeado):
        super().__init__()
        self.title("Compra de Entradas")
        self.usuario_logeado = usuario_logeado

        self.db = get_db()
        self.coleccion_transacciones = self.db["transacciones"]

        self.usuarios = obtener_usuarios()
        self.peliculas = obtener_peliculas()

        self.label_disponibilidad = tk.Label(self, text="Disponibilidad: NA")
        self.label_disponibilidad.grid(row=3, column=2, padx=10)

        self.label_precio_unitario = tk.Label(self, text=f"Precio por entrada: ${PRECIO_ENTRADA}")
        self.label_precio_unitario.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        self.label_precio_total = tk.Label(self, text=f"Total: ${PRECIO_ENTRADA}")
        self.label_precio_total.grid(row=4, column=2, columnspan=2)

        self.recibo_text = tk.Text(self, height=12, width=60, cursor="arrow")

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
        self.combo_cantidad = ttk.Combobox(self, values=[str(i) for i in range(1, 11)], state="readonly")
        self.combo_cantidad.grid(row=3, column=1)
        self.combo_cantidad.set("1")
        self.combo_cantidad.bind("<<ComboboxSelected>>", self.actualizar_precio_total)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Continuar con el pago", command=self.mostrar_pasarela_pago)\
            .pack(side="left", padx=10)

        tk.Button(btn_frame, text="Regresar", command=self.destroy)\
            .pack(side="left", padx=10)

        self.recibo_text = tk.Text(self, height=12, width=60)
        self.recibo_text.grid(row=6, column=0, columnspan=3)
        
    def cargar_funciones(self, event=None):
        pelicula_nombre = self.pelicula_combo.get()
        self.funcion_combo.set('')
        self.funcion_combo['values'] = []
        self.label_disponibilidad.config(text="Disponibilidad: NA")

        pelicula = next((p for p in self.peliculas if p["nombre"] == pelicula_nombre), None)
        if pelicula:
            horas = [f["hora"] + f" (Disp: {f['disponibles']})" for f in pelicula["funciones"]]
            self.funcion_combo['values'] = horas

    def actualizar_precio_total(self, event=None):
        try:
            cantidad = int(self.combo_cantidad.get())
            total = cantidad * PRECIO_ENTRADA
            self.label_precio_total.config(text=f"Total: ${total:,}")
        except ValueError:
            self.label_precio_total.config(text="Total: $0")

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
        

    def mostrar_pasarela_pago(self):
        self.ventana_pago = tk.Toplevel(self)
        self.ventana_pago.title("Pasarela de Pago")

        tk.Label(self.ventana_pago, text="Número de tarjeta:").pack()
        self.entry_tarjeta = tk.Entry(self.ventana_pago)
        self.entry_tarjeta.pack()

        tk.Label(self.ventana_pago, text="Fecha de vencimiento (MM/AA):").pack()
        self.entry_vencimiento = tk.Entry(self.ventana_pago)
        self.entry_vencimiento.pack()

        tk.Label(self.ventana_pago, text="CVC:").pack()
        self.entry_cvc = tk.Entry(self.ventana_pago, show="*")
        self.entry_cvc.pack()

        tk.Button(self.ventana_pago, text="Confirmar y pagar", command=self.procesar_pago).pack(pady=10)

    def procesar_pago(self):
        tarjeta = self.entry_tarjeta.get()
        vencimiento = self.entry_vencimiento.get()
        cvc = self.entry_cvc.get()

        if not (tarjeta and vencimiento and cvc):
            messagebox.showerror("Error", "Complete los datos de la tarjeta")
            return

        self.ventana_pago.destroy()

        if self.usuario_logeado["rol"] == "admin":
            correo_usuario = self.usuario_combo.get()
            usuario = next((u for u in self.usuarios if u["correo"] == correo_usuario), None)
        else:
            usuario = self.usuario_logeado
            correo_usuario = usuario["correo"]

        pelicula_nombre = self.pelicula_combo.get()
        funcion_hora = self.funcion_combo.get()
        cantidad_str = self.combo_cantidad.get()

        if not correo_usuario or not pelicula_nombre or not funcion_hora or not cantidad_str:
            messagebox.showerror("Error", "Complete todos los campos", parent=self)
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

        hora_real = funcion_hora.split(" ")[0]

        exito, mensaje = comprar_entrada(str(usuario["_id"]), str(pelicula["_id"]), hora_real, cantidad)
        if exito:
            total = cantidad * PRECIO_ENTRADA

            transaccion = {
                "usuario_id": usuario["_id"],
                "usuario_correo": usuario["correo"],
                "pelicula_id": pelicula["_id"],
                "pelicula_nombre": pelicula["nombre"],
                "hora_funcion": hora_real,
                "cantidad": cantidad,
                "total_pagado": total,
                "tarjeta": tarjeta[-4:],  # Últimos 4 dígitos
                "fecha": datetime.now()
            }
            self.coleccion_transacciones.insert_one(transaccion)

            self.mostrar_recibo(usuario, pelicula, hora_real, cantidad, total, mensaje)

            self.peliculas = obtener_peliculas()
            self.cargar_funciones()
            self.funcion_combo.set(funcion_hora)
            self.actualizar_disponibilidad()
        else:
            messagebox.showerror("Error", mensaje, parent=self)

    def mostrar_recibo(self, usuario, pelicula, hora, cantidad, total, mensaje):
        self.recibo_text.delete("1.0", tk.END)
        self.recibo_text.config(state="normal")
        texto = (
            f"FACTURA\n"
            f"Usuario: {usuario['nombre']} ({usuario['correo']})\n"
            f"Película: {pelicula['nombre']}\n"
            f"Función: {hora}\n"
            f"Cantidad: {cantidad}\n"
            f"Total pagado: ${total:,}\n"
            f"{mensaje}\n"
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Gracias por su compra!"
        )
        self.recibo_text.insert(tk.END, texto)
        self.recibo_text.config(state="disabled")
