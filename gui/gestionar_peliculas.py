import tkinter as tk
from tkinter import messagebox
from models.pelicula import agregar_pelicula, obtener_peliculas, eliminar_pelicula, editar_pelicula
from bson.objectid import ObjectId

def ventana_gestion_peliculas():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Películas")

    # --- Formulario agregar/editar ---
    tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=0, column=1)

    tk.Label(ventana, text="Género:").grid(row=1, column=0)
    entry_genero = tk.Entry(ventana)
    entry_genero.grid(row=1, column=1)

    tk.Label(ventana, text="Duración (min):").grid(row=2, column=0)
    entry_duracion = tk.Entry(ventana)
    entry_duracion.grid(row=2, column=1)

    tk.Label(ventana, text="Funciones (hora,disponibles separados por coma; usa ';' entre funciones):").grid(row=3, column=0, columnspan=2)
    entry_funciones = tk.Entry(ventana, width=50)
    entry_funciones.grid(row=4, column=0, columnspan=2)

    # Para editar
    pelicula_edit_id = None

    def cargar_datos_pelicula(pelicula):
        nonlocal pelicula_edit_id
        pelicula_edit_id = str(pelicula["_id"])
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
        nonlocal pelicula_edit_id
        pelicula_edit_id = None
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

        if pelicula_edit_id:
            exito = editar_pelicula(pelicula_edit_id, nombre, genero, duracion, funciones)
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

    btn_frame = tk.Frame(ventana)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

    btn_guardar = tk.Button(btn_frame, text="Guardar película", command=guardar_pelicula)
    btn_guardar.pack(side="left", padx=10)

    btn_regresar = tk.Button(btn_frame, text="Regresar", command=ventana.destroy)
    btn_regresar.pack(side="left", padx=10)
    # --- Lista de películas ---
    frame_lista = tk.Frame(ventana)
    frame_lista.grid(row=6, column=0, columnspan=2)

    def mostrar_peliculas():
        for widget in frame_lista.winfo_children():
            widget.destroy()

        peliculas = obtener_peliculas()

        for i, peli in enumerate(peliculas):
            tk.Label(frame_lista, text=peli["nombre"]).grid(row=i, column=0)
            tk.Label(frame_lista, text=peli["genero"]).grid(row=i, column=1)
            tk.Label(frame_lista, text=peli["duracion"]).grid(row=i, column=2)

            btn_editar = tk.Button(frame_lista, text="Editar", command=lambda p=peli: cargar_datos_pelicula(p))
            btn_editar.grid(row=i, column=3)

            btn_eliminar = tk.Button(frame_lista, text="Eliminar", command=lambda p=peli: eliminar_y_actualizar(p))
            btn_eliminar.grid(row=i, column=4)

    def eliminar_y_actualizar(pelicula):
        if messagebox.askyesno("Confirmar", f"¿Eliminar película '{pelicula['nombre']}'?"):
            eliminado = eliminar_pelicula(str(pelicula["_id"]))
            if eliminado:
                messagebox.showinfo("Éxito", "Película eliminada")
                mostrar_peliculas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la película")

    mostrar_peliculas()
