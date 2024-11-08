import tkinter as tk
import random
import json

def obtener_usuario_sesion():
    try:
        with open('Commons/usuario_sesion.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos.get('usuario', 'sin_usuario')
    except FileNotFoundError:
        return 'sin_usuario'

class VentanaFacturaEfectivo:
    def __init__(self, carrito, total, nombre_cliente=None):
        self.carrito = carrito
        self.total = total
        # Asigna el usuario de sesión como nombre de cliente
        self.nombre_cliente = obtener_usuario_sesion()
        self.codigo_retiro = self.generar_codigo_retiro()

        # Configuración de la ventana
        self.ventana_factura = tk.Toplevel()
        self.ventana_factura.title("Factura de Pago en Efectivo")
        self.ventana_factura.geometry("400x500")
        self.ventana_factura.configure(bg="#FFFFFF")

        # Título de la factura
        label_titulo = tk.Label(self.ventana_factura, text="Factura de Pago en Efectivo", font=("Arial", 16, "bold"), bg="#FFFFFF")
        label_titulo.pack(pady=10)

        # Mostrar el nombre del cliente
        # Mostrar el nombre del cliente obtenido de la sesión
        label_nombre = tk.Label(self.ventana_factura, text=f"Cliente: {self.nombre_cliente}", font=("Arial", 12),bg="#FFFFFF")
        label_nombre.pack(pady=5)

        # Mensaje de retiro en almacén
        label_retiro = tk.Label(self.ventana_factura, text="Deberá retirar los productos en el almacén.",
                                font=("Arial", 12), bg="#FFFFFF", fg="black")
        label_retiro.pack(pady=10)

        # Nuevo mensaje sobre los días de retiro
        label_dias_retiro = tk.Label(self.ventana_factura, text="Retiro únicamente martes y jueves.",
                                     font=("Arial", 12), bg="#FFFFFF", fg="black")
        label_dias_retiro.pack(pady=5)

        # Mostrar los productos
        label_productos = tk.Label(self.ventana_factura, text="Productos:", font=("Arial", 12, "bold"), bg="#FFFFFF")
        label_productos.pack(pady=5)

        for item in self.carrito:
            item_texto = f"{item['nombre']} - Cantidad: {item['cantidad']} - Precio: {item['precio'] * item['cantidad']}"
            label_item = tk.Label(self.ventana_factura, text=item_texto, font=("Arial", 10), bg="#FFFFFF")
            label_item.pack()

        # Mostrar el código de retiro
        label_codigo = tk.Label(self.ventana_factura, text=f"Código de retiro: {self.codigo_retiro}",
        font=("Arial", 12, "bold"), bg="#FFFFFF", fg="black")
        label_codigo.pack(pady=10)

        # Mostrar el total
        label_total = tk.Label(self.ventana_factura, text=f"Total pagado: {self.total}", font=("Arial", 12, "bold"),
                               bg="#FFFFFF")
        label_total.pack(pady=10)

        # Botón para cerrar la factura
        boton_cerrar = tk.Button(self.ventana_factura, text="Cerrar Factura", command=self.cerrar_factura, fg="black")
        boton_cerrar.pack(pady=20)

    def generar_codigo_retiro(self):
        # Genera un código de retiro aleatorio de 6 dígitos
        return str(random.randint(100000, 999999))

    def cerrar_factura(self):
        # Cierra la ventana de la factura
        self.ventana_factura.destroy()