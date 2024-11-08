import tkinter as tk
from tkinter import messagebox
from Pantallas.Compra.ventana_factura_tarj import VentanaFactura
from datetime import datetime


class VentanaTarjeta:
    def __init__(self, carrito, total):
        self.carrito = carrito
        self.total = total  # Guardamos el total en la clase

        self.ventana_tarjeta = tk.Toplevel()
        self.ventana_tarjeta.title("Ingreso de Datos de la Tarjeta")
        self.ventana_tarjeta.geometry("400x500")
        self.ventana_tarjeta.configure(bg="#FCC509")

        label_titulo = tk.Label(self.ventana_tarjeta, text="Ingrese los Datos de la Tarjeta", font=("Arial", 14),
                                bg="#FCC509", fg="black")
        label_titulo.pack(pady=10)

        # Campos de entrada para los datos de la tarjeta
        self.label_numero = tk.Label(self.ventana_tarjeta, text="Número de Tarjeta:", bg="#FCC509", fg="black")
        self.label_numero.pack(pady=5)
        self.entry_numero = tk.Entry(self.ventana_tarjeta, width=30)
        self.entry_numero.pack(pady=5)

        self.label_vencimiento = tk.Label(self.ventana_tarjeta, text="Fecha Vencimiento (MM/AA):", bg="#FCC509",
                                          fg="black")
        self.label_vencimiento.pack(pady=5)
        self.entry_vencimiento = tk.Entry(self.ventana_tarjeta, width=30)
        self.entry_vencimiento.pack(pady=5)

        self.label_codigo = tk.Label(self.ventana_tarjeta, text="Código de Seguridad:", bg="#FCC509", fg="black")
        self.label_codigo.pack(pady=5)
        self.entry_codigo = tk.Entry(self.ventana_tarjeta, width=30, show="*")  # show="*" para ocultar el código
        self.entry_codigo.pack(pady=5)

        self.label_nombre = tk.Label(self.ventana_tarjeta, text="Nombre del Propietario:", bg="#FCC509", fg="black")
        self.label_nombre.pack(pady=5)
        self.entry_nombre = tk.Entry(self.ventana_tarjeta, width=30)
        self.entry_nombre.pack(pady=5)

        self.label_direccion = tk.Label(self.ventana_tarjeta, text="Dirección del Propietario:", bg="#FCC509",
                                        fg="black")
        self.label_direccion.pack(pady=5)
        self.entry_direccion = tk.Entry(self.ventana_tarjeta, width=30)
        self.entry_direccion.pack(pady=5)

        # Mostrar el total de la compra
        label_total = tk.Label(self.ventana_tarjeta, text=f"Total de la Compra: ${self.total:.2f}", bg="#FCC509",
                               fg="black")
        label_total.pack(pady=20)

        # Botón para confirmar la información de la tarjeta
        boton_confirmar = tk.Button(self.ventana_tarjeta, text="Confirmar", command=self.confirmar_pago, bg="green",
                                    fg="white", width=15)
        boton_confirmar.pack(pady=20)

    def confirmar_pago(self):
        # Obtener los datos de los campos
        numero = self.entry_numero.get()
        vencimiento = self.entry_vencimiento.get()
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        direccion = self.entry_direccion.get()

        # Validar el número de tarjeta (debe tener exactamente 16 dígitos)
        if not numero.isdigit() or len(numero) != 16:
            messagebox.showerror("Error", "Número de tarjeta inválido.")
            return

        # Validar la fecha de vencimiento (debe ser MM/AA)
        if not vencimiento.isdigit() or len(vencimiento) != 4:
            messagebox.showerror("Error", "Fecha de vencimiento inválida.")
            return

        # Validar los demás campos
        if not codigo or not nombre or not direccion:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Calcular el total nuevamente si es necesario
        if not hasattr(self, 'total') or self.total is None:
            total = sum(item['precio'] * item['cantidad'] for item in self.carrito)
        else:
            total = self.total

        # Confirmar el pago con mensaje de éxito
        messagebox.showinfo("Pago Confirmado", f"Pago con tarjeta de {nombre} confirmado.")

        # Mostrar la factura
        VentanaFactura(self.carrito, total, direccion)

        # Liberar el carrito después del pago
        self.carrito.clear()  # Limpiar el carrito

        # Cerrar la ventana de tarjeta
        self.ventana_tarjeta.destroy()

