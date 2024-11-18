import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Pantallas.Compra.metodo_pago import MetodoPagoVentana


class CarritoVentana:
    def __init__(self, carrito, productos):
        # Guardar el carrito, productos y crear la ventana
        self.carrito = carrito
        self.productos = productos  # Lista de productos disponibles
        self.carrito_ventana = tk.Toplevel()
        self.carrito_ventana.title("Carrito de Compras")
        self.carrito_ventana.geometry("500x700")
        self.carrito_ventana.configure(bg="#FCC509")

        # Crear los elementos de la interfaz
        self.crear_widgets()

        # Actualizar el contenido del carrito al abrir la ventana
        self.actualizar_carrito()

    def crear_widgets(self):
        # Título del carrito
        label_carrito = tk.Label(self.carrito_ventana, text="Carrito de Compras", font=("Arial", 18), bg="#FCC509",
                                 fg="black")
        label_carrito.pack(pady=10)

        # Treeview para mostrar productos
        self.tree = ttk.Treeview(self.carrito_ventana, columns=('Nombre', 'Precio', 'Cantidad', 'Total'),
                                 show='headings')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Total', text='Total')

        self.tree.column('Nombre', width=150)
        self.tree.column('Precio', width=80)
        self.tree.column('Cantidad', width=80)
        self.tree.column('Total', width=80)

        self.tree.pack(expand=True, fill='both', pady=20)

        # Botones para agregar y eliminar productos
        boton_agregar = tk.Button(self.carrito_ventana, text="Agregar Producto", command=self.agregar_producto,
                                  bg="green", fg="white", width=15)
        boton_agregar.pack(pady=5)

        boton_eliminar = tk.Button(self.carrito_ventana, text="Eliminar Producto", command=self.eliminar_producto,
                                   bg="red", fg="white", width=15)
        boton_eliminar.pack(pady=5)

        # Etiqueta para el total del carrito
        self.label_total = tk.Label(self.carrito_ventana, text="", font=("Arial", 14), bg="#FCC509", fg="black")
        self.label_total.pack()

        # Botón para comprar
        boton_comprar = tk.Button(self.carrito_ventana, text="Comprar", command=self.abrir_metodo_pago, bg="blue",
                                  fg="white", width=15)
        boton_comprar.pack(pady=10)

        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(self.carrito_ventana, text="Cerrar", command=self.carrito_ventana.destroy, bg="white",
                                 fg="black", width=15)
        boton_cerrar.pack(pady=10)

    def actualizar_carrito(self):
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Calcular y mostrar el total del carrito
        total_carrito = 0
        for item in self.carrito:
            total_producto = item['precio'] * item['cantidad']
            total_carrito += total_producto
            self.tree.insert('', tk.END, values=(item['nombre'], f"₡{item['precio']:.2f}", item['cantidad'],
                                                 f"₡{total_producto:.2f}"))

        # Actualizar el texto del total
        self.label_total.config(text=f"Total: ₡{total_carrito:.2f}")

    def eliminar_producto(self):
        # Obtener el producto seleccionado
        selected_item = self.tree.selection()
        if selected_item:
            # Obtener el índice del producto en la lista carrito
            index = self.tree.index(selected_item[0])
            if self.carrito[index]['cantidad'] > 1:
                self.carrito[index]['cantidad'] -= 1
            else:
                self.carrito.pop(index)  # Eliminar el producto si la cantidad es 1

            # Actualizar la vista y el total
            self.actualizar_carrito()

    def agregar_producto(self):
        # Obtener el producto seleccionado
        selected_item = self.tree.selection()
        if selected_item:
            # Obtener el índice del producto en la lista carrito
            index = self.tree.index(selected_item[0])

            nombre_producto = self.carrito[index]['nombre']
            cantidad_actual = self.carrito[index]['cantidad']

            # Buscar el producto en el inventario para obtener la cantidad disponible
            producto_en_inventario = next((p for p in self.productos if p['nombre'] == nombre_producto), None)

            if producto_en_inventario:
                cantidad_disponible = producto_en_inventario['cantidad']

                # Verificar si se puede agregar más productos
                if cantidad_actual < cantidad_disponible:
                    self.carrito[index]['cantidad'] += 1  # Aumentar la cantidad en el carrito
                else:
                    # Si no hay suficiente stock, mostrar un mensaje
                    self.mostrar_mensaje("No se puede agregar más productos", f"Solo hay {cantidad_disponible} disponibles de {nombre_producto}.")
            else:
                self.mostrar_mensaje("Producto no encontrado", "El producto no está disponible en el inventario.")

            # Actualizar la vista y el total
            self.actualizar_carrito()

    def mostrar_mensaje(self, titulo, mensaje):
        # Mostrar un mensaje emergente con el título y el mensaje
        messagebox.showinfo(titulo, mensaje)

    def abrir_metodo_pago(self):
        # Abre la ventana de métodos de pago
        MetodoPagoVentana(self.carrito)

    def obtener_total(self):
        total_carrito = 0
        for item in self.carrito:
            total_carrito += item['precio'] * item['cantidad']
        return total_carrito


# Ejemplo de uso
def abrir_carrito(carrito, productos):
    CarritoVentana(carrito, productos)
