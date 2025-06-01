import tkinter as tk
from tkinter import messagebox
from servicios.pelicula import agregar_pelicula, obtener_peliculas, eliminar_pelicula, editar_pelicula
from estilos import *

def ventana_gestion_peliculas():
    """Crea la ventana de gestión de películas."""
    ventana = tk.Toplevel()
    aplicar_estilos_ventana(ventana, "Gestión de Películas")

    pelicula_edit_id = [None]  # Para almacenar id de la película que se edita

    # Entradas
    entry_nombre = crear_entry(ventana)
    entry_genero = crear_entry(ventana)
    entry_duracion = crear_entry(ventana)
    entry_funciones = crear_entry(ventana)
    entry_funciones.config(width=50)

    def crear_formulario():
        crear_label(ventana, "Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_nombre.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        crear_label(ventana, "Género:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_genero.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        crear_label(ventana, "Duración (min):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_duracion.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        crear_label(ventana, "Funciones (hora,disponibles separados por coma; usa ';' entre funciones):").grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=(10,5))
        entry_funciones.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def cargar_datos_pelicula(pelicula):
        pelicula_edit_id[0] = str(pelicula["_id"])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, pelicula["nombre"])
        entry_genero.delete(0, tk.END)
        entry_genero.insert(0, pelicula["genero"])
        entry_duracion.delete(0, tk.END)
        entry_duracion.insert(0, pelicula["duracion"])
        funciones_str = "; ".join([f'{f["hora"]},{f["disponibles"]}' for f in pelicula["funciones"]])
        entry_funciones.delete(0, tk.END)
        entry_funciones.insert(0, funciones_str)

    def limpiar_formulario():
        pelicula_edit_id[0] = None
        entry_nombre.delete(0, tk.END)
        entry_genero.delete(0, tk.END)
        entry_duracion.delete(0, tk.END)
        entry_funciones.delete(0, tk.END)

    def guardar_pelicula():
        nombre = entry_nombre.get()
        genero = entry_genero.get()
        try:
            duracion = int(entry_duracion.get())
        except ValueError:
            messagebox.showerror("Error", "La duración debe ser un número")
            return

        funciones_raw = entry_funciones.get()
        funciones = []
        try:
            for f in funciones_raw.split(";"):
                hora, disponibles = f.strip().split(",")
                funciones.append({"hora": hora.strip(), "disponibles": int(disponibles.strip())})
        except Exception:
            messagebox.showerror("Error", "Formato incorrecto en funciones. Ejemplo: 18:00,80; 21:00,60")
            return

        if pelicula_edit_id[0]:
            exito = editar_pelicula(pelicula_edit_id[0], nombre, genero, duracion, funciones)
            if exito:
                messagebox.showinfo("Éxito", "Película actualizada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo actualizar la película")
        else:
            exito = agregar_pelicula(nombre, genero, duracion, funciones)
            if exito:
                messagebox.showinfo("Éxito", "Película agregada correctamente")

        limpiar_formulario()
        mostrar_peliculas()

    def eliminar_y_actualizar(pelicula):
        if messagebox.askyesno("Confirmar", f"¿Eliminar película '{pelicula['nombre']}'?"):
            eliminado = eliminar_pelicula(str(pelicula["_id"]))
            if eliminado:
                messagebox.showinfo("Éxito", "Película eliminada")
                mostrar_peliculas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la película")

    def mostrar_peliculas():
        for widget in frame_lista.winfo_children():
            widget.destroy()

        peliculas = obtener_peliculas()
        for i, peli in enumerate(peliculas):
            crear_label(frame_lista, peli["nombre"]).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            crear_label(frame_lista, peli["genero"]).grid(row=i, column=1, sticky="w", padx=5, pady=2)
            crear_label(frame_lista, str(peli["duracion"])).grid(row=i, column=2, sticky="w", padx=5, pady=2)

            btn_edit = crear_boton(frame_lista, "Editar", lambda p=peli: cargar_datos_pelicula(p))
            btn_edit.grid(row=i, column=3, padx=5, pady=2)

            btn_del = crear_boton(frame_lista, "Eliminar", lambda p=peli: eliminar_y_actualizar(p), color=COLOR_ROJO)
            btn_del.grid(row=i, column=4, padx=5, pady=2)

    def crear_botones():
        btn_frame = tk.Frame(ventana, bg=COLOR_FONDO)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        btn_guardar = crear_boton(btn_frame, "Guardar película", guardar_pelicula)
        btn_guardar.pack(side="left", padx=10)

        btn_regresar = crear_boton(btn_frame, "Regresar", ventana.destroy, color=COLOR_ROJO)
        btn_regresar.pack(side="left", padx=10)

    crear_formulario()
    crear_botones()

    frame_lista = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_lista.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_rowconfigure(6, weight=1)

    mostrar_peliculas()
