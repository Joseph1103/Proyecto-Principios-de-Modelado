import tkinter as tk
from tkinter import ttk, messagebox
import os
import json


def abrir_clasificador(root):
    # Crear una nueva ventana del clasificador
    clasificador_ventana = tk.Toplevel(root)
    clasificador_ventana.title("Clasificador")
    clasificador_ventana.geometry("800x600")
    clasificador_ventana.configure(bg="#FCC509")

    # Título de la ventana del clasificador
    label_clasificador = tk.Label(clasificador_ventana, text="Bienvenido Operador", font=("Arial", 22), bg="#FCC509",
                                  fg="black")
    label_clasificador.pack(pady=50)

    # Botón para abrir la ventana de Clasificador
    boton_clasificador = tk.Button(clasificador_ventana, text="Clasificador",
                                   command=lambda: abrir_ventana_clasificador(clasificador_ventana, root),
                                   bg="white", fg="#B90518", width=25, height=2)
    boton_clasificador.pack(pady=10)

    # Botón para abrir la ventana de BOM
    boton_bom = tk.Button(clasificador_ventana, text="BOM",
                          command=lambda: abrir_ventana_bom(clasificador_ventana, root),
                          bg="white", fg="#B90518", width=25, height=2)
    boton_bom.pack(pady=10)

    # Botón para cerrar la ventana del clasificador y volver a la ventana principal
    boton_cerrar = tk.Button(clasificador_ventana, text="Cerrar Clasificador",
                             command=lambda: cerrar_clasificador(root, clasificador_ventana),
                             bg="white", fg="#B90518", width=25, height=2)
    boton_cerrar.pack(pady=20)


def abrir_ventana_bom(parent, root):
    # Cierra la ventana principal del clasificador
    parent.withdraw()

    # Crear una nueva ventana para la funcionalidad de BOM
    ventana_bom = tk.Toplevel(root)
    ventana_bom.title("Ventana BOM")
    ventana_bom.geometry("600x500")
    ventana_bom.configure(bg="#FCC509")

    # Título de la ventana BOM
    label = tk.Label(ventana_bom, text="BOM", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=20)

    # Cargar los datos de BOM desde el archivo JSON
    ruta_bom = os.path.join("Commons", "boms.json")
    ruta_inventario = os.path.join("Commons", "inventario.json")
    try:
        with open(ruta_bom, "r") as file:
            data = json.load(file)  # Cargar el archivo JSON como un diccionario
            productos = data.get("productos", [])
        with open(ruta_inventario, "r") as inv_file:
            inventario = json.load(inv_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No se pudo cargar el archivo de inventario o BOM.")
        ventana_bom.destroy()
        parent.deiconify()
        return

    # Diccionario para mapear cada código de producto con sus materiales y cantidades
    recetas = {producto["codigoProducto"]: producto for producto in productos}

    # Frame para los campos de Código y Cantidad
    frame = tk.Frame(ventana_bom, bg="#FCC509")
    frame.pack(pady=10)

    # Label y ComboBox para seleccionar el Código
    codigo_label = tk.Label(frame, text="Código:", font=("Arial", 14), bg="#FCC509", fg="black")
    codigo_label.grid(row=0, column=0, padx=10, pady=5)

    # ComboBox para los códigos, usando las claves en el diccionario recetas
    codigo_selector = ttk.Combobox(frame, values=list(recetas.keys()), font=("Arial", 12), width=20)
    codigo_selector.grid(row=0, column=1, padx=10, pady=5)

    # Label y Entry para la cantidad
    cantidad_label = tk.Label(frame, text="Cantidad a producir:", font=("Arial", 14), bg="#FCC509", fg="black")
    cantidad_label.grid(row=1, column=0, padx=10, pady=5)

    cantidad_entry = tk.Entry(frame, font=("Arial", 12), width=22)
    cantidad_entry.grid(row=1, column=1, padx=10, pady=5)

    # Tabla de materiales y cantidad necesaria
    table_frame = tk.Frame(ventana_bom, bg="#FCC509")
    table_frame.pack(pady=20)

    materiales_label = tk.Label(table_frame, text="Materiales", font=("Arial", 12, "bold"), bg="white", fg="black",
                                width=20)
    materiales_label.grid(row=0, column=0, padx=1, pady=1)

    cantidad_necesaria_label = tk.Label(table_frame, text="Cantidad Necesaria", font=("Arial", 12, "bold"), bg="white",
                                        fg="black", width=20)
    cantidad_necesaria_label.grid(row=0, column=1, padx=1, pady=1)

    # Función para mostrar la receta cuando se selecciona un código
    def mostrar_receta(event):
        # Limpiar las filas anteriores
        for widget in table_frame.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()

        # Obtener el código seleccionado
        codigo = codigo_selector.get()
        producto = recetas.get(codigo)

        if producto:
            materiales = producto["materiales"]

            # Mostrar los materiales y cantidades en la tabla
            for i, material in enumerate(materiales, start=1):
                tk.Label(table_frame, text=material["codigoMaterial"], font=("Arial", 12), bg="white", fg="black",
                         width=20).grid(row=i, column=0, padx=1, pady=1)
                tk.Label(table_frame, text=f"{material['cantidad']} {material['unidadMedida']}", font=("Arial", 12),
                         bg="white", fg="black", width=20).grid(row=i, column=1, padx=1, pady=1)

    # Asociar la selección de código con la función mostrar_receta
    codigo_selector.bind("<<ComboboxSelected>>", mostrar_receta)

    # Función para producir la receta
    def producir():
        codigo = codigo_selector.get()
        try:
            cantidad_producir = int(cantidad_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida para producir.")
            return

        producto = recetas.get(codigo)

        if not producto:
            messagebox.showerror("Error", "Seleccione un código de producto válido.")
            return

        # Calcular el total de materiales necesarios
        for material in producto["materiales"]:
            codigo_material = material["codigoMaterial"]
            cantidad_necesaria = material["cantidad"] * cantidad_producir

            if inventario.get(codigo_material, 0) < cantidad_necesaria:
                messagebox.showerror("Error", f"No hay suficiente {codigo_material} en el inventario.")
                return

        # Descontar los materiales del inventario
        for material in producto["materiales"]:
            codigo_material = material["codigoMaterial"]
            cantidad_necesaria = material["cantidad"] * cantidad_producir
            inventario[codigo_material] -= cantidad_necesaria

        # Guardar el inventario actualizado
        with open(ruta_inventario, "w") as inv_file:
            json.dump(inventario, inv_file)

        messagebox.showinfo("Producción", f"Se ha producido {cantidad_producir} de {codigo}.")

    # Botón para producir
    boton_producir = tk.Button(ventana_bom, text="Producir", command=producir, bg="green", fg="white", width=15,
                               height=2)
    boton_producir.pack(pady=10)

    # Botón para abrir la ventana de Almacén
    boton_almacen = tk.Button(ventana_bom, text="Almacén", command=lambda: abrir_almacen(ventana_bom, root),
                              bg="white", fg="#B90518", width=15, height=2)
    boton_almacen.pack(pady=10)

    # Botón para volver a la ventana del clasificador
    boton_volver = tk.Button(ventana_bom, text="Volver", command=lambda: regresar_al_clasificador(ventana_bom, parent),
                             bg="white", fg="#B90518", width=15, height=1)
    boton_volver.pack(pady=10)


def abrir_almacen(parent, root):
    # Cierra la ventana BOM
    parent.withdraw()

    # Crear una nueva ventana para la funcionalidad de Almacén
    ventana_almacen = tk.Toplevel(root)
    ventana_almacen.title("Almacén")
    ventana_almacen.geometry("800x600")
    ventana_almacen.configure(bg="#FCC509")

    # Título de la ventana Almacén
    label = tk.Label(ventana_almacen, text="Inventario de Almacén", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=20)

    # Ruta al archivo de inventario
    ruta_inventario = os.path.join("Commons", "inventario.json")

    # Cargar el inventario
    try:
        with open(ruta_inventario, "r") as inv_file:
            inventario = json.load(inv_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No se pudo cargar el archivo de inventario.")
        ventana_almacen.destroy()
        parent.deiconify()
        return

    # Frame para mostrar el inventario en una tabla
    frame = tk.Frame(ventana_almacen, bg="#FCC509")
    frame.pack(pady=10)

    # Columnas de la tabla
    tk.Label(frame, text="Código", font=("Arial", 12, "bold"), bg="white", fg="black", width=15).grid(row=0, column=0,
                                                                                                      padx=5, pady=5)
    tk.Label(frame, text="Cantidad", font=("Arial", 12, "bold"), bg="white", fg="black", width=15).grid(row=0, column=1,
                                                                                                        padx=5, pady=5)
    tk.Label(frame, text="Modificar", font=("Arial", 12, "bold"), bg="white", fg="black", width=15).grid(row=0,
                                                                                                         column=2,
                                                                                                         padx=5, pady=5)

    # Mostrar cada item del inventario con una entrada para modificar la cantidad
    entry_widgets = {}
    for i, (codigo, cantidad) in enumerate(inventario.items(), start=1):
        tk.Label(frame, text=codigo, font=("Arial", 12), bg="white", fg="black", width=15).grid(row=i, column=0, padx=5,
                                                                                                pady=5)
        cantidad_label = tk.Label(frame, text=str(cantidad), font=("Arial", 12), bg="white", fg="black", width=15)
        cantidad_label.grid(row=i, column=1, padx=5, pady=5)
        entry = tk.Entry(frame, font=("Arial", 12), width=15)
        entry.grid(row=i, column=2, padx=5, pady=5)
        entry_widgets[codigo] = (cantidad_label, entry)

    # Función para actualizar el inventario
    def actualizar_inventario():
        for codigo, (cantidad_label, entry) in entry_widgets.items():
            # Verifica que el campo no esté vacío antes de intentar actualizar
            if entry.get().strip():  # Si el campo no está vacío
                try:
                    ajuste = int(entry.get())  # Convierte el ajuste a entero
                    inventario[codigo] += ajuste  # Suma o resta la cantidad en inventario
                    cantidad_label.config(text=str(inventario[codigo]))  # Actualiza la etiqueta de cantidad
                    entry.delete(0, tk.END)  # Limpia el campo de entrada
                except ValueError:
                    messagebox.showerror("Error", f"Ingrese un número válido para {codigo}")
                    return

        # Guardar el inventario actualizado en el archivo JSON
        with open(ruta_inventario, "w") as inv_file:
            json.dump(inventario, inv_file)

        messagebox.showinfo("Inventario Actualizado", "El inventario ha sido actualizado correctamente.")

    # Botón para aplicar los cambios al inventario
    boton_actualizar = tk.Button(ventana_almacen, text="Actualizar Inventario", command=actualizar_inventario,
                                 bg="green", fg="white", width=20, height=2)
    boton_actualizar.pack(pady=10)

    # Botón para volver a la ventana de BOM
    boton_volver = tk.Button(ventana_almacen, text="Volver", command=lambda: regresar_al_bom(ventana_almacen, parent),
                             bg="white", fg="#B90518", width=15, height=1)
    boton_volver.pack(pady=10)


def regresar_al_bom(ventana_actual, ventana_bom):
    ventana_actual.destroy()  # Cierra la ventana actual (Almacén)
    ventana_bom.deiconify()  # Vuelve a mostrar la ventana BOM


def regresar_al_clasificador(ventana_actual, clasificador_ventana):
    ventana_actual.destroy()  # Cierra la ventana actual (BOM o Clasificador)
    clasificador_ventana.deiconify()  # Vuelve a mostrar la ventana principal del clasificador


def cerrar_clasificador(root, clasificador_ventana):
    clasificador_ventana.destroy()  # Cierra la ventana del clasificador
    root.deiconify()  # Muestra de nuevo la ventana principal
