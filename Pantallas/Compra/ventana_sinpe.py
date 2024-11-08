import tkinter as tk
from tkinter import messagebox
from Pantallas.Compra.ventana_factura_sinpe import VentanaFacturaSinpe  # Importamos la clase de la factura


class VentanaSinpe:
    def __init__(self, carrito, total):
        self.carrito = carrito
        self.total = total
        self.ventana_sinpe = tk.Toplevel()
        self.ventana_sinpe.title("Pago con SINPE Móvil")
        self.ventana_sinpe.geometry("400x400")
        self.ventana_sinpe.configure(bg="#FCC509")

        label_titulo = tk.Label(self.ventana_sinpe, text="Realiza el pago a través de SINPE Móvil", font=("Arial", 14),
                                bg="#FCC509", fg="black")
        label_titulo.pack(pady=20)

        # Mostrar el número de SINPE al que se debe realizar el pago
        label_sinpe = tk.Label(self.ventana_sinpe, text="Hacer el SINPE Móvil al número: 83005821", font=("Arial", 12),
                               bg="#FCC509", fg="black")
        label_sinpe.pack(pady=10)

        # Ingresar la dirección si el usuario no está registrado
        label_direccion = tk.Label(self.ventana_sinpe, text="Dirección para la entrega:", bg="#FCC509", fg="black")
        label_direccion.pack(pady=5)
        self.entry_direccion = tk.Entry(self.ventana_sinpe)
        self.entry_direccion.pack(pady=5)

        # Botón para confirmar el pago con SINPE
        boton_confirmar = tk.Button(self.ventana_sinpe, text="SINPE Móvil Realizado", command=self.confirmar_pago_sinpe,
                                    bg="green", fg="white", width=20)
        boton_confirmar.pack(pady=20)

    def confirmar_pago_sinpe(self):
        # Dirección ingresada
        direccion = self.entry_direccion.get()

        # Simula la confirmación del pago
        messagebox.showinfo("Pago Confirmado", "Pago realizado con SINPE Móvil al número 83005821.")

        # Generar la factura y mostrarla
        VentanaFacturaSinpe(self.carrito, self.total, direccion)

        # Limpiar el carrito
        self.carrito.clear()

        # Cierra la ventana después de confirmar el pago
        self.ventana_sinpe.destroy()