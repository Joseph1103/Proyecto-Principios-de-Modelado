import tkinter as tk
from tkinter import ttk, messagebox


class TiendaApp:
    def __init__(self, file_path):
        self.file_path = file_path
        self.articulos = self.leer_articulos()
        self.articulos_rebajados = []  # Lista para almacenar los artículos rebajados
        self.root = tk.Toplevel()  # Crear una nueva ventana secundaria
        self.root.title("Tienda - Rebajas de artículos")

        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Tabla de artículos
        self.columns = ("Nombre", "Precio", "Cantidad")
        self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings", height=10)
        self.tree.pack(side="left")
        for col in self.columns:
            self.tree.heading(col, text=col)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=self.scrollbar.set)

        # Entradas de rebaja y cantidad con etiquetas
        label_rebaja = tk.Label(self.root, text="Rebaja (%)")
        label_rebaja.pack(pady=5)

        self.entry_rebaja = tk.Entry(self.root, width=10)
        self.entry_rebaja.pack(pady=5)

        label_cantidad = tk.Label(self.root, text="Cantidad")
        label_cantidad.pack(pady=5)

        self.entry_cantidad = tk.Entry(self.root, width=10)
        self.entry_cantidad.pack(pady=5)

        # Botón para aplicar rebaja
        self.btn_aplicar = tk.Button(self.root, text="Aplicar Rebaja", command=self.aplicar_rebaja)
        self.btn_aplicar.pack(pady=10)

        # Botón para revertir rebaja
        self.btn_revertir = tk.Button(self.root, text="Revertir Rebaja", command=self.revertir_rebaja)
        self.btn_revertir.pack(pady=10)

        self.btn_cerrar = tk.Button(self.root, text="Cerrar", command=self.root.destroy, bg="red", fg="white")
        self.btn_cerrar.pack(pady=10)

        # Cargar datos iniciales
        self.cargar_articulos()

    def leer_articulos(self):
        """Lee los artículos del archivo y los devuelve como una lista."""
        try:
            with open(self.file_path, "r") as file:
                # Procesa cada línea y convierte los valores
                return [
                    [
                        line.strip().split(", ")[0],  # Nombre
                        int(float(line.strip().split(", ")[1])),  # Precio, eliminando decimales
                        int(float(line.strip().split(", ")[2]))  # Cantidad, asegurando que sea un entero
                    ] for line in file.readlines()
                ]
        except FileNotFoundError:
            return []

    def escribir_articulos(self):
        """Sobrescribe el archivo con los artículos actuales, excluyendo los artículos rebajados revertidos."""
        with open(self.file_path, "w") as file:
            # Escribir los artículos originales (sin decimales en precio o cantidad)
            for articulo in self.articulos:
                file.write(", ".join(map(str, [articulo[0], int(articulo[1]), int(articulo[2])])) + "\n")

            # Escribir los artículos rebajados que no han sido revertidos
            for rebajado in self.articulos_rebajados:
                nombre, precio, cantidad = rebajado["articulo_rebajado"]
                # Asegurar que el precio y la cantidad sean enteros
                file.write(", ".join([nombre, str(int(precio)), str(int(cantidad))]) + "\n")

    def cargar_articulos(self):
        """Carga los artículos en la tabla de la interfaz."""
        # Limpiar la tabla antes de cargar los artículos
        self.tree.delete(*self.tree.get_children())

        # Cargar artículos originales
        for articulo in self.articulos:
            # Eliminar decimales del precio y asegurar que la cantidad sea un entero
            articulo[1] = int(articulo[1])  # El precio como entero
            articulo[2] = int(articulo[2])  # La cantidad como entero
            self.tree.insert("", "end", values=articulo)

        # Cargar los artículos rebajados en la tabla
        for rebajado in self.articulos_rebajados:
            nombre, precio, cantidad = rebajado["articulo_rebajado"]
            self.tree.insert("", "end", values=[nombre, int(precio), int(cantidad)])

    def aplicar_rebaja(self):
        """Aplica una rebaja a un artículo seleccionado y lo agrega a la lista de artículos rebajados."""
        try:
            seleccion = self.tree.selection()[0]
            articulo = self.tree.item(seleccion, "values")
            nombre, precio, cantidad = articulo

            # Entrada para rebaja
            rebaja = float(self.entry_rebaja.get())
            nueva_cantidad = int(self.entry_cantidad.get())
            cantidad_original = int(cantidad)

            if rebaja < 0 or rebaja > 100:
                messagebox.showerror("Error", "La rebaja debe ser entre 0 y 100.")
                return

            if nueva_cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                return

            if nueva_cantidad > cantidad_original:
                messagebox.showerror("Error", "No hay suficiente cantidad en stock.")
                return

            # Calcular nuevo precio rebajado, redondeando a un entero
            precio_original = float(precio)
            precio_rebajado = round(precio_original * (1 - rebaja / 100))  # Redondear al entero más cercano

            # Verificar si ya existe una rebaja para este artículo
            for rebajado in self.articulos_rebajados:
                if rebajado["nombre"] == nombre:
                    messagebox.showerror("Error", "Este artículo ya tiene una rebaja aplicada.")
                    return

            # Crear una copia del artículo con el precio rebajado y la cantidad reducida
            articulo_rebajado = [nombre + " (rebajado " + str(rebaja) + "%)", precio_rebajado, nueva_cantidad]

            # Agregar el artículo rebajado a la lista de rebajados
            self.articulos_rebajados.append(
                {"nombre": nombre, "rebaja": rebaja, "precio_original": precio_original, "cantidad": nueva_cantidad,
                 "articulo_rebajado": articulo_rebajado})

            # Actualizar la cantidad del producto original en la lista de artículos
            nueva_cantidad_original = cantidad_original - nueva_cantidad
            index = self.tree.index(seleccion)  # Obtener el índice antes de eliminar el elemento
            self.articulos[index][2] = str(nueva_cantidad_original)

            # Escribir los cambios al archivo
            self.escribir_articulos()

            # Recargar la tabla de artículos
            self.cargar_articulos()

            messagebox.showinfo("Éxito", "Rebaja aplicada correctamente.")

        except IndexError:
            messagebox.showerror("Error", "Por favor, selecciona un artículo.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos para rebaja y cantidad.")

    def revertir_rebaja(self):
        """Revierte la rebaja de un artículo y lo devuelve a su precio y cantidad original."""
        try:
            seleccion = self.tree.selection()[0]
            articulo = self.tree.item(seleccion, "values")
            nombre, precio, cantidad = articulo

            # Buscar la promoción relacionada con el artículo rebajado
            promocion = next((p for p in self.articulos_rebajados if nombre.startswith(p["nombre"])), None)

            if not promocion:
                messagebox.showerror("Error", "Este artículo no tiene rebaja aplicada.")
                return

            # Revertir el precio y la cantidad del artículo
            precio_original = promocion["precio_original"]
            cantidad_original = promocion["cantidad"]  # Revertir al valor de la cantidad rebajada

            # Buscar el artículo original en la lista de artículos
            index = next((i for i, art in enumerate(self.articulos) if art[0] == promocion["nombre"]), None)

            if index is not None:
                # Sumar la cantidad revertida
                cantidad_actual = int(self.articulos[index][2])
                self.articulos[index][1] = precio_original  # Revertir el precio
                self.articulos[index][2] = str(cantidad_actual + cantidad_original)  # Sumar la cantidad original

                # Eliminar el artículo rebajado de la lista de artículos rebajados
                self.articulos_rebajados = [p for p in self.articulos_rebajados if p["articulo_rebajado"][0] != nombre]

                # Escribir los cambios al archivo
                self.escribir_articulos()

                # Recargar la tabla de artículos
                self.cargar_articulos()

                messagebox.showinfo("Éxito", "Rebaja revertida correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró el artículo original para revertir la rebaja.")

        except IndexError:
            messagebox.showerror("Error", "Por favor, selecciona un artículo para revertir la rebaja.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


# Función que abrirá la ventana de promociones
def abrir_promociones():
    TiendaApp("Commons/articulos.txt")

