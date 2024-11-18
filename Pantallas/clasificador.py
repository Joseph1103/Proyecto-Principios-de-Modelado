import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from .clasificacion import abrir_clasificacion
from Pantallas.historial_recibos import abrir_historial_compras



# Mapeo de códigos de inventario a los nombres en la tienda
MAPEO_CODIGOS_TIENDA = {
    "TOM-001": "Tomates 1Kg",
    "PAP-001": "Papas 1Kg",
    "SLT-001": "Salsa de tomate enlatada 400g",
    "SLT-002": "Salsa de tomate enlatada 1kg",
    "SAL-001": "Salsa de tomate envasada 500ml",
    "SAL-002": "Salsa de tomate envasada 1L",
    "CHP-001": "Chips de papa 200g",
    "CHP-002": "Chips de papa 500g",
}

def abrir_clasificador(root):
    clasificador_ventana = tk.Toplevel(root)
    clasificador_ventana.title("Clasificador")
    clasificador_ventana.geometry("800x600")
    clasificador_ventana.configure(bg="#FCC509")

    label_clasificador = tk.Label(clasificador_ventana, text="Bienvenido Operador", font=("Arial", 22), bg="#FCC509", fg="black")
    label_clasificador.pack(pady=50)

    boton_clasificador = tk.Button(clasificador_ventana, text="Clasificador", command=lambda: abrir_clasificacion(clasificador_ventana),
                                   bg="white", fg="#B90518", width=25, height=2)
    boton_clasificador.pack(pady=10)

    boton_bom = tk.Button(clasificador_ventana, text="BOM", command=lambda: abrir_ventana_bom(clasificador_ventana, root),
                          bg="white", fg="#B90518", width=25, height=2)
    boton_bom.pack(pady=10)

    boton_historial = tk.Button(clasificador_ventana, text="Historial de Compras", command=lambda: abrir_historial_compras(),
                                bg="white", fg="#B90518", width=25, height=2)
    boton_historial.pack(pady=20)

    boton_cerrar = tk.Button(clasificador_ventana, text="Cerrar Clasificador", command=lambda: cerrar_clasificador(root, clasificador_ventana),
                             bg="white", fg="#B90518", width=25, height=2)
    boton_cerrar.pack(pady=20)


def abrir_ventana_bom(parent, root):
    parent.withdraw()

    ventana_bom = tk.Toplevel(root)
    ventana_bom.title("Ventana BOM")
    ventana_bom.geometry("600x500")
    ventana_bom.configure(bg="#FCC509")

    label = tk.Label(ventana_bom, text="BOM", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=20)

    ruta_bom = os.path.join("Commons", "boms.json")
    ruta_inventario = os.path.join("Commons", "inventario.json")

    try:
        with open(ruta_bom, "r") as file:
            data = json.load(file)
            productos = data.get("productos", [])
        with open(ruta_inventario, "r") as inv_file:
            inventario = json.load(inv_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No se pudo cargar el archivo de inventario o BOM.")
        ventana_bom.destroy()
        parent.deiconify()
        return

    recetas = {producto["codigoProducto"]: producto for producto in productos}

    frame = tk.Frame(ventana_bom, bg="#FCC509")
    frame.pack(pady=10)

    codigo_label = tk.Label(frame, text="Código:", font=("Arial", 14), bg="#FCC509", fg="black")
    codigo_label.grid(row=0, column=0, padx=10, pady=5)

    codigo_selector = ttk.Combobox(frame, values=list(recetas.keys()), font=("Arial", 12), width=20)
    codigo_selector.grid(row=0, column=1, padx=10, pady=5)

    cantidad_label = tk.Label(frame, text="Cantidad a producir:", font=("Arial", 14), bg="#FCC509", fg="black")
    cantidad_label.grid(row=1, column=0, padx=10, pady=5)

    cantidad_entry = tk.Entry(frame, font=("Arial", 12), width=22)
    cantidad_entry.grid(row=1, column=1, padx=10, pady=5)

    table_frame = tk.Frame(ventana_bom, bg="#FCC509")
    table_frame.pack(pady=20)

    materiales_label = tk.Label(table_frame, text="Materiales", font=("Arial", 12, "bold"), bg="white", fg="black", width=20)
    materiales_label.grid(row=0, column=0, padx=1, pady=1)

    cantidad_necesaria_label = tk.Label(table_frame, text="Cantidad Necesaria", font=("Arial", 12, "bold"), bg="white", fg="black", width=20)
    cantidad_necesaria_label.grid(row=0, column=1, padx=1, pady=1)

    def mostrar_receta(event):
        for widget in table_frame.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()

        codigo = codigo_selector.get()
        producto = recetas.get(codigo)
        if producto:
            for i, material in enumerate(producto["materiales"], start=1):
                tk.Label(table_frame, text=material["codigoMaterial"], font=("Arial", 12), bg="white", fg="black", width=20).grid(row=i, column=0, padx=1, pady=1)
                tk.Label(table_frame, text=f"{material['cantidad']} {material['unidadMedida']}", font=("Arial", 12), bg="white", fg="black", width=20).grid(row=i, column=1, padx=1, pady=1)

    codigo_selector.bind("<<ComboboxSelected>>", mostrar_receta)

    def producir():
        codigo = codigo_selector.get()
        try:
            cantidad_producir = int(cantidad_entry.get())
            if cantidad_producir <= 0:
                messagebox.showerror("Error", "Ingrese una cantidad válida mayor a cero para producir.")
                return
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida para producir.")
            return

        if not codigo or codigo not in recetas:
            messagebox.showerror("Error", "Seleccione un código válido.")
            return

        producto = recetas.get(codigo)
        if not producto:
            messagebox.showerror("Error", "Seleccione un código de producto válido.")
            return

        materiales = producto["materiales"]

        # Verificar si hay suficientes materiales en el inventario
        cantidad_maxima = float('inf')
        ingrediente_faltante = None

        for material in materiales:
            codigo_material = material["codigoMaterial"]
            cantidad_necesaria = material["cantidad"] * cantidad_producir

            inventario_actual = inventario.get(codigo_material, 0)
            if inventario_actual < cantidad_necesaria:
                # Calcular la cantidad máxima que se puede producir
                cantidad_posible = inventario_actual // material["cantidad"]
                if cantidad_posible < cantidad_maxima:
                    cantidad_maxima = cantidad_posible
                    ingrediente_faltante = codigo_material

        # Si no se puede producir ni una unidad
        if cantidad_maxima == 0:
            messagebox.showerror("Error", f"No se pudo procesar ninguna unidad. Falta {ingrediente_faltante}.")
            return

        # Ajustar la cantidad a producir si no hay suficientes materiales
        if cantidad_maxima < cantidad_producir:
            messagebox.showwarning(
                "Producción Parcial",
                f"Solo se pudieron procesar {cantidad_maxima} unidades porque falta {ingrediente_faltante}."
            )
            cantidad_producir = cantidad_maxima

            # Terminar la función después de mostrar el mensaje de advertencia
            return

        # Descontar los materiales del inventario según la cantidad a producir
        for material in materiales:
            codigo_material = material["codigoMaterial"]
            cantidad_necesaria = material["cantidad"] * cantidad_producir

            # Descontar la cantidad necesaria del inventario
            inventario[codigo_material] = max(0, inventario.get(codigo_material, 0) - cantidad_necesaria)

        # Agregar las unidades producidas al inventario del producto final
        inventario[codigo] = inventario.get(codigo, 0) + cantidad_producir

        # Guardar el inventario actualizado
        with open(ruta_inventario, "w") as inv_file:
            json.dump(inventario, inv_file)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Producción", f"Se han producido {cantidad_producir} unidades de {codigo}.")

    boton_producir = tk.Button(ventana_bom, text="Producir", command=producir, bg="green", fg="white", width=15, height=2)
    boton_producir.pack(pady=10)

    def abrir_almacen():
        abrir_ventana_almacen(ventana_bom, root)

    boton_almacen = tk.Button(ventana_bom, text="Almacén", command=abrir_almacen, bg="blue", fg="white", width=15, height=2)
    boton_almacen.pack(pady=10)

    boton_volver = tk.Button(ventana_bom, text="Volver", command=lambda: regresar_al_clasificador(ventana_bom, parent),
                             bg="white", fg="#B90518", width=15, height=1)
    boton_volver.pack(pady=10)


def abrir_ventana_almacen(parent, root):
    parent.withdraw()

    ventana_almacen = tk.Toplevel(root)
    ventana_almacen.title("Almacén")
    ventana_almacen.geometry("800x600")
    ventana_almacen.configure(bg="#FCC509")

    label = tk.Label(ventana_almacen, text="Inventario de Almacén", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=10)

    # Continuación de funciones relacionadas al almacén

# Cierre de ventanas y otros elementos faltantes.

def abrir_ventana_almacen(parent, root):
    parent.withdraw()

    ventana_almacen = tk.Toplevel(root)
    ventana_almacen.title("Almacén")
    ventana_almacen.geometry("800x600")
    ventana_almacen.configure(bg="#FCC509")

    label = tk.Label(ventana_almacen, text="Inventario de Almacén", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=10)

    ruta_inventario = os.path.join("Commons", "inventario.json")
    ruta_articulos = os.path.join("Commons", "articulos.txt")

    try:
        with open(ruta_inventario, "r") as inv_file:
            inventario = json.load(inv_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No se pudo cargar el archivo de inventario.")
        ventana_almacen.destroy()
        parent.deiconify()
        return

    frame = tk.Frame(ventana_almacen, bg="#FCC509")
    frame.pack(pady=10)

    tk.Label(frame, text="Código", font=("Arial", 10, "bold"), bg="white", fg="black", width=12).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="Cantidad", font=("Arial", 10, "bold"), bg="white", fg="black", width=12).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame, text="Modificar", font=("Arial", 10, "bold"), bg="white", fg="black", width=12).grid(row=0, column=2, padx=5, pady=5)
    tk.Label(frame, text="Enviar a tienda", font=("Arial", 10, "bold"), bg="white", fg="black", width=15).grid(row=0, column=3, padx=5, pady=5)

    entry_widgets = {}
    enviar_widgets = {}
    for i, (codigo, cantidad) in enumerate(inventario.items(), start=1):
        tk.Label(frame, text=codigo, font=("Arial", 10), bg="white", fg="black", width=12).grid(row=i, column=0, padx=5, pady=2)
        cantidad_label = tk.Label(frame, text=str(cantidad), font=("Arial", 10), bg="white", fg="black", width=12)
        cantidad_label.grid(row=i, column=1, padx=5, pady=2)
        entry = tk.Entry(frame, font=("Arial", 10), width=12)
        entry.grid(row=i, column=2, padx=5, pady=2)
        entry_widgets[codigo] = (cantidad_label, entry)

        enviar_entry = tk.Entry(frame, font=("Arial", 10), width=12)
        enviar_entry.grid(row=i, column=3, padx=5, pady=2)
        enviar_widgets[codigo] = enviar_entry

    def actualizar_inventario():
        for codigo, (cantidad_label, entry) in entry_widgets.items():
            if entry.get().strip():
                try:
                    ajuste = int(entry.get())
                    # Actualizar el inventario sin permitir valores negativos
                    inventario[codigo] = max(0, inventario.get(codigo, 0) + ajuste)
                    cantidad_label.config(text=str(inventario[codigo]))  # Actualizar visualmente
                    entry.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("Error", f"Ingrese un número válido para {codigo}")
                    return

        # Guardar el inventario actualizado en el archivo
        with open(ruta_inventario, "w") as inv_file:
            json.dump(inventario, inv_file)

        # Refrescar visualmente los datos del inventario
        for codigo, (cantidad_label, _) in entry_widgets.items():
            cantidad_label.config(text=str(inventario[codigo]))

        messagebox.showinfo("Inventario Actualizado", "El inventario ha sido actualizado correctamente.")

    def enviar_a_tienda():
        try:
            with open(ruta_articulos, "r") as art_file:
                articulos = []
                for line in art_file:
                    partes = line.strip().split(", ")
                    if len(partes) != 3:
                        continue
                    nombre = partes[0]
                    try:
                        precio = int(partes[1])
                        cantidad = int(partes[2])
                    except ValueError:
                        continue
                    articulos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
        except FileNotFoundError:
            articulos = []

        for codigo, enviar_entry in enviar_widgets.items():
            if codigo not in MAPEO_CODIGOS_TIENDA:
                continue

            if enviar_entry.get().strip():
                try:
                    enviar_cantidad = int(enviar_entry.get())
                    if enviar_cantidad > inventario.get(codigo, 0):
                        messagebox.showerror("Error",
                                             f"No hay suficiente cantidad de {codigo} en el almacén para enviar.")
                        return
                    # Actualizar inventario sin permitir valores negativos
                    inventario[codigo] = max(0, inventario[codigo] - enviar_cantidad)

                    articulo_encontrado = False
                    for articulo in articulos:
                        if articulo["nombre"] == MAPEO_CODIGOS_TIENDA[codigo]:
                            articulo["cantidad"] += enviar_cantidad
                            articulo_encontrado = True
                            break

                    if not articulo_encontrado:
                        articulos.append(
                            {"nombre": MAPEO_CODIGOS_TIENDA[codigo], "precio": 0, "cantidad": enviar_cantidad})

                    enviar_entry.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("Error", f"Ingrese un número válido para {codigo}")
                    return

        # Guardar cambios en archivos
        with open(ruta_articulos, "w") as art_file:
            for articulo in articulos:
                art_file.write(f"{articulo['nombre']}, {articulo['precio']}, {articulo['cantidad']}\n")

        with open(ruta_inventario, "w") as inv_file:
            json.dump(inventario, inv_file)

        # Refrescar visualmente los datos del inventario
        for codigo, (cantidad_label, _) in entry_widgets.items():
            cantidad_label.config(text=str(inventario[codigo]))

        messagebox.showinfo("Éxito", "Los productos han sido enviados a la tienda correctamente.")

    boton_actualizar = tk.Button(ventana_almacen, text="Actualizar Inventario", command=actualizar_inventario, bg="green", fg="white", width=20, height=2)
    boton_actualizar.pack(pady=10)

    boton_enviar = tk.Button(ventana_almacen, text="Enviar a tienda", command=enviar_a_tienda, bg="blue", fg="white", width=20, height=2)
    boton_enviar.pack(pady=10)

    boton_volver = tk.Button(ventana_almacen, text="Volver", command=lambda: regresar_al_bom(ventana_almacen, parent),
                             bg="white", fg="#B90518", width=15, height=1)
    boton_volver.pack(pady=10)


def regresar_al_bom(ventana_actual, ventana_bom):
    ventana_actual.destroy()
    ventana_bom.deiconify()


def regresar_al_clasificador(ventana_actual, clasificador_ventana):
    ventana_actual.destroy()
    clasificador_ventana.deiconify()


def cerrar_clasificador(root, clasificador_ventana):
    clasificador_ventana.destroy()
    root.deiconify()