import tkinter as tk
from Pantallas.Compra.ventana_tarjeta import VentanaTarjeta
from Pantallas.Compra.ventana_sinpe import VentanaSinpe
from Pantallas.Compra.ventana_factura_efectivo import VentanaFacturaEfectivo

class MetodoPagoVentana:
    def __init__(self, carrito):
        self.carrito = carrito
        self.pago_ventana = tk.Toplevel()
        self.pago_ventana.title("Método de Pago")
        self.pago_ventana.geometry("300x250")
        self.pago_ventana.configure(bg="#FCC509")

        label_titulo = tk.Label(self.pago_ventana, text="Seleccione el Método de Pago", font=("Arial", 14), bg="#FCC509", fg="black")
        label_titulo.pack(pady=20)

        # Botones para los métodos de pago
        boton_tarjeta = tk.Button(self.pago_ventana, text="Tarjeta", command=self.pagar_con_tarjeta, bg="blue", fg="white", width=15)
        boton_tarjeta.pack(pady=10)

        boton_sinpe = tk.Button(self.pago_ventana, text="SINPE Móvil", command=self.pagar_con_sinpe, bg="green", fg="white", width=15)
        boton_sinpe.pack(pady=10)

        boton_efectivo = tk.Button(self.pago_ventana, text="Efectivo", command=self.pagar_con_efectivo, bg="orange", fg="black", width=15)
        boton_efectivo.pack(pady=10)

    def pagar_con_tarjeta(self):
        # Calcular el total antes de hacer el pago
        total = sum(item['precio'] * item['cantidad'] for item in self.carrito)
        self.pago_ventana.destroy()  # Cierra la ventana de métodos de pago
        VentanaTarjeta(self.carrito, total)  # Pasar el carrito y el total a la ventana de tarjeta

    def pagar_con_sinpe(self):
        # Calcular el total antes de hacer el pago
        total = sum(item['precio'] * item['cantidad'] for item in self.carrito)
        self.pago_ventana.destroy()  # Cierra la ventana de métodos de pago
        VentanaSinpe(self.carrito, total)  # Pasar el carrito y el total a la ventana de SINPE

    def pagar_con_efectivo(self):
        # Calcula el total antes de generar la factura
        total = sum(item['precio'] * item['cantidad'] for item in self.carrito)

        # Obtener el nombre del cliente (puedes pedirlo mediante un cuadro de diálogo o usar un campo almacenado)
        nombre_cliente = "Cliente no registrado"

        # Abrir la ventana de factura para el pago en efectivo
        VentanaFacturaEfectivo(self.carrito, total, nombre_cliente)

        self.actualizar_inventario_txt()
        # Limpiar el carrito después de generar la factura
        self.carrito.clear()

    def actualizar_inventario_txt(self):
        try:
            # Cargar el inventario actual
            with open('Commons/articulos.txt', 'r') as archivo:
                lineas = archivo.readlines()

            # Crear un diccionario para los productos en el inventario
            inventario = {}
            for linea in lineas:
                if linea.strip():  # Ignorar líneas vacías
                    partes = linea.strip().split(', ')
                    if len(partes) == 3:  # Asegurar que haya 3 valores
                        nombre, precio, cantidad = partes
                        inventario[nombre] = {'precio': int(precio), 'cantidad': int(cantidad)}
                    else:
                        print(f"Línea mal formateada: {linea.strip()}")  # Opcional: Log de errores

            # Restar la cantidad comprada del inventario
            for item in self.carrito:
                if item['nombre'] in inventario:
                    inventario[item['nombre']]['cantidad'] -= item['cantidad']

            productos_a_eliminar = [nombre for nombre, datos in inventario.items() if datos['cantidad'] == 0]
            for producto in productos_a_eliminar:
                del inventario[producto]

            # Guardar el inventario actualizado
            with open('Commons/articulos.txt', 'w') as archivo:
                for nombre, datos in inventario.items():
                    archivo.write(f"{nombre}, {datos['precio']}, {datos['cantidad']}\n")

        except FileNotFoundError:
            print("Error: No se encontró el archivo de inventario.")
        except Exception as e:
            print(f"Error: {e}")
