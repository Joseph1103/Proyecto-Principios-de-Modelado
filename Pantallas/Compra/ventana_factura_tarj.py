import random
import string
import tkinter as tk
from tkinter import messagebox
import json


def obtener_usuario_sesion():
    """Lee el archivo de sesión y retorna el nombre de usuario o 'sin_usuario' si no ha iniciado sesión."""
    try:
        with open('Commons/usuario_sesion.json', 'r') as archivo:
            datos = json.load(archivo)
            usuario = datos.get('usuario', 'sin_usuario')  # Devuelve el nombre del usuario o 'sin_usuario'

            # Imprimir el nombre del usuario para depuración
            print(f"Nombre de usuario obtenido: {usuario}")

            return usuario
    except FileNotFoundError:
        # Imprimir un mensaje si el archivo no se encuentra
        print("Archivo de sesión no encontrado. Asignando 'sin_usuario'.")
        return 'sin_usuario'


class VentanaFactura:
    def __init__(self, carrito, total, direccion_propietario):
        self.carrito = carrito
        self.total = total
        self.usuario = obtener_usuario_sesion()  # Obtener el usuario de la sesión
        self.direccion_propietario = direccion_propietario  # Dirección del propietario
        self.ventana_factura = tk.Toplevel()
        self.ventana_factura.title("Factura de Compra")
        self.ventana_factura.geometry("400x500")  # Ajusté el tamaño para caber toda la información
        self.ventana_factura.configure(bg="#FCC509")
        self.crear_widgets()

    def generar_codigo_retiro(self):
        """Genera un código único de retiro para usuarios sin sesión."""
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return codigo

    def crear_widgets(self):
        label_titulo = tk.Label(self.ventana_factura, text="Factura de Compra", font=("Arial", 14), bg="#FCC509", fg="black")
        label_titulo.pack(pady=20)

        # Mostrar el nombre del usuario o 'sin_usuario'
        label_usuario = tk.Label(self.ventana_factura, text=f"Usuario: {self.usuario}", bg="#FCC509", fg="black")
        label_usuario.pack(pady=5)

        # Si el usuario no ha iniciado sesión, generar un código y mostrar mensaje de retiro en almacén
        if self.usuario == "sin_usuario":
            codigo_retiro = self.generar_codigo_retiro()  # Generar código único
            label_direccion = tk.Label(self.ventana_factura, text="Dirección: Retiro en almacén", bg="#FCC509", fg="black")
            label_direccion.pack(pady=5)
            label_codigo = tk.Label(self.ventana_factura, text=f"Código de retiro: {codigo_retiro}", bg="#FCC509", fg="black")
            label_codigo.pack(pady=5)
        else:
            # Mostrar la dirección del propietario
            label_direccion = tk.Label(self.ventana_factura, text=f"Dirección: {self.direccion_propietario}", bg="#FCC509", fg="black")
            label_direccion.pack(pady=5)

        # Mostrar los productos del carrito
        for item in self.carrito:
            label_producto = tk.Label(self.ventana_factura, text=f"{item['nombre']} - {item['cantidad']} x ₡{item['precio']:.2f}", bg="#FCC509", fg="black")
            label_producto.pack()

        # Mostrar el total
        label_total = tk.Label(self.ventana_factura, text=f"Total: ₡{self.total:.2f}", font=("Arial", 14), bg="#FCC509", fg="black")
        label_total.pack(pady=10)

        boton_cerrar = tk.Button(self.ventana_factura, text="Cerrar", command=self.ventana_factura.destroy, fg="black", width=15)
        boton_cerrar.pack(pady=10)


