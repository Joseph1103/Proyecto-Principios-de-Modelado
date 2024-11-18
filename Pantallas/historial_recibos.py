import tkinter as tk
import json


class HistorialCompras:
    def __init__(self, archivo_historial):
        self.archivo_historial = archivo_historial
        self.historial = self.cargar_historial()

    def cargar_historial(self):
        try:
            # Intentamos abrir el archivo JSON y cargar los datos
            with open(self.archivo_historial, 'r') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            # Si el archivo no existe, devolvemos una lista vacía
            return []
        except json.JSONDecodeError:
            # Si hay un error en el formato del JSON, devolvemos una lista vacía
            return []

    def mostrar_historial(self):
        # Crea la ventana del historial de compras
        historial_ventana = tk.Toplevel()
        historial_ventana.title("Historial de Compras")
        historial_ventana.geometry("800x600")  # Tamaño fijo de la ventana
        historial_ventana.configure(bg="#F5F5F5")

        # Título del historial
        label_historial = tk.Label(historial_ventana, text="Historial de Compras", font=("Arial", 18), bg="#F5F5F5",
                                   fg="black")
        label_historial.pack(pady=10)

        # Creamos un Canvas para el contenido del historial con un marco scrollable
        canvas = tk.Canvas(historial_ventana)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Barra de desplazamiento
        scrollbar = tk.Scrollbar(historial_ventana, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Asociamos el scrollbar con el canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Creamos un frame dentro del canvas
        frame_historial = tk.Frame(canvas, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        canvas.create_window((0, 0), window=frame_historial, anchor="nw")

        # Si no hay historial, mostramos un mensaje
        if not self.historial:
            tk.Label(frame_historial, text="No tienes compras aún.", bg="#FFFFFF", anchor="w").pack(fill=tk.X, padx=5,
                                                                                                    pady=2)
        else:
            for compra in self.historial:
                cliente = compra.get("cliente", "Desconocido")
                fecha = compra.get("fecha", "Fecha no disponible")
                metodo_pago = compra.get("Método de pago", "No especificado")
                total = compra.get("total", 0)
                productos = compra.get("productos", [])

                info_compra = f"Cliente: {cliente} | Fecha: {fecha} | Método de Pago: {metodo_pago} | Total: ₡{total}"
                tk.Label(frame_historial, text=info_compra, bg="#FFFFFF", anchor="w", font=("Arial", 10, "bold")).pack(
                    fill=tk.X, padx=5, pady=5)

                for producto in productos:
                    detalle_producto = f"  {producto['nombre']} - Cantidad: {producto['cantidad']} - Precio: ₡{producto['precio']}"
                    tk.Label(frame_historial, text=detalle_producto, bg="#FFFFFF", anchor="w").pack(fill=tk.X, padx=15,
                                                                                                    pady=2)

                tk.Label(frame_historial, text="-" * 60, bg="#FFFFFF").pack(fill=tk.X, padx=5, pady=5)

        # Actualizamos la región del canvas para que se ajuste al contenido
        frame_historial.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Frame para el botón de cerrar, fuera del área scrollable
        frame_boton = tk.Frame(historial_ventana, bg="#F5F5F5")
        frame_boton.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Botón para cerrar el historial
        boton_cerrar = tk.Button(frame_boton, text="Cerrar", command=historial_ventana.destroy, bg="white",
                                 fg="#B90518", width=20)
        boton_cerrar.pack()


# Crear una instancia global para el historial
historial_compras = HistorialCompras('Commons/historial_compras.json')


def abrir_historial_compras():
    historial_compras.mostrar_historial()
