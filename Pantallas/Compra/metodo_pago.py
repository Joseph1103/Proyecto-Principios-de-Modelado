import tkinter as tk
from Pantallas.Compra.ventana_tarjeta import VentanaTarjeta  # Importamos la clase VentanaTarjeta
from Pantallas.Compra.ventana_sinpe import VentanaSinpe  # Importamos la ventana de SINPE Móvil

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
        print("Pago en efectivo seleccionado.")