import tkinter as tk
from tkinter import messagebox
import json
import random

# Función para obtener el estado de la sesión
def obtener_usuario_sesion():
    try:
        with open('Commons/usuario_sesion.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos.get('usuario', 'sin_usuario')
    except FileNotFoundError:
        return 'sin_usuario'

class VentanaFacturaSinpe:
    def __init__(self, carrito, total, direccion_propietario):
        self.carrito = carrito
        self.total = total
        self.usuario = obtener_usuario_sesion()
        self.direccion_propietario = direccion_propietario
        self.ventana_factura = tk.Toplevel()
        self.ventana_factura.title("Factura de Compra")
        self.ventana_factura.geometry("400x600")
        self.ventana_factura.configure(bg="#FCC509")
        self.crear_widgets()

    def crear_widgets(self):
        label_titulo = tk.Label(self.ventana_factura, text="Factura de Compra", font=("Arial", 14), bg="#FCC509", fg="black")
        label_titulo.pack(pady=20)

        # Mostrar el nombre del usuario o 'sin_usuario'
        label_usuario = tk.Label(self.ventana_factura, text=f"Usuario: {self.usuario}", bg="#FCC509", fg="black")
        label_usuario.pack(pady=5)

        # Mostrar la dirección del propietario o mensaje de recogida
        if self.usuario == "sin_usuario":
            codigo_retiro = f"COD-{random.randint(1000, 9999)}"
            label_direccion = tk.Label(self.ventana_factura, text="Dirección: Recoger en almacén", bg="#FCC509", fg="black")
            label_codigo = tk.Label(self.ventana_factura, text=f"Código de retiro: {codigo_retiro}", bg="#FCC509", fg="black")
            label_direccion.pack(pady=5)
            label_codigo.pack(pady=5)
        else:
            label_direccion = tk.Label(self.ventana_factura, text=f"Dirección: {self.direccion_propietario}", bg="#FCC509", fg="black")
            label_direccion.pack(pady=5)

        # Mostrar los productos del carrito
        for item in self.carrito:
            label_producto = tk.Label(self.ventana_factura, text=f"{item['nombre']} - {item['cantidad']} x ${item['precio']:.2f}", bg="#FCC509", fg="black")
            label_producto.pack()

        # Mostrar el total
        label_total = tk.Label(self.ventana_factura, text=f"Total: ${self.total:.2f}", font=("Arial", 14), bg="#FCC509", fg="black")
        label_total.pack(pady=10)

        boton_cerrar = tk.Button(self.ventana_factura, text="Cerrar", command=self.ventana_factura.destroy, fg="black", width=15)
        boton_cerrar.pack(pady=10)