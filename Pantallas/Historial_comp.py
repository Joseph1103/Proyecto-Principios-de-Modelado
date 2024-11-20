import tkinter as tk
import json


# Función para obtener el usuario de sesión desde un archivo JSON
def obtener_usuario_sesion():
    try:
        with open('Commons/usuario_sesion.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos.get('usuario', 'sin_usuario')
    except FileNotFoundError:
        return 'sin_usuario'


class HistorialCompras:
    def __init__(self, archivo_historial):
        self.archivo_historial = archivo_historial

    def cargar_historial(self):
        try:
            with open(self.archivo_historial, 'r') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def mostrar_historial(self):
        # Cargar el historial actualizado cada vez que se abre la ventana
        self.historial = self.cargar_historial()
        usuario_actual = obtener_usuario_sesion()

        if usuario_actual == 'sin_usuario':
            self.mostrar_mensaje("No iniciaste sesión", "Para ver el historial, necesitas iniciar sesión.")
            return

        historial_filtrado = [compra for compra in self.historial if compra.get("cliente") == usuario_actual]

        historial_ventana = tk.Toplevel()
        historial_ventana.title("Historial de Compras")
        historial_ventana.geometry("610x750")
        historial_ventana.configure(bg="#F5F5F5")

        # Encabezado
        label_historial = tk.Label(historial_ventana, text="Historial de Compras", font=("Arial", 18), bg="#F5F5F5",
                                   fg="black")
        label_historial.pack(pady=5)  # Espaciado más pequeño

        # Crear un Canvas para el contenido del historial con un tamaño limitado en el eje Y
        canvas = tk.Canvas(historial_ventana, height=400, bg="#F5F5F5")  # Limitar la altura del canvas
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)

        # Barra de desplazamiento
        scrollbar = tk.Scrollbar(historial_ventana, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Asociar el scrollbar con el canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un frame dentro del canvas
        frame_historial = tk.Frame(canvas, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        canvas.create_window((0, 0), window=frame_historial, anchor="nw")

        if not historial_filtrado:
            tk.Label(frame_historial, text="No tienes compras aún.", bg="#FFFFFF", anchor="w").pack(fill=tk.X, padx=5,
                                                                                                    pady=2)
        else:
            for compra in historial_filtrado:
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

        # Actualizamos el área del Canvas para ajustarse al contenido
        frame_historial.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Botón para cerrar el historial, centrado
        boton_cerrar = tk.Button(historial_ventana, text="Cerrar", command=historial_ventana.destroy, bg="white",
                                 fg="#B90518", width=20)
        boton_cerrar.pack(side=tk.BOTTOM, pady=10, anchor="center")

    def mostrar_mensaje(self, titulo, mensaje):
        mensaje_ventana = tk.Toplevel()
        mensaje_ventana.title(titulo)
        mensaje_ventana.geometry("400x200")
        mensaje_ventana.configure(bg="#F5F5F5")

        label_mensaje = tk.Label(mensaje_ventana, text=mensaje, font=("Arial", 14), bg="#F5F5F5", fg="black")
        label_mensaje.pack(pady=50)

        boton_cerrar = tk.Button(mensaje_ventana, text="Cerrar", command=mensaje_ventana.destroy, bg="white",
                                 fg="#B90518", width=20)
        boton_cerrar.pack(pady=10)


# Crear una instancia del historial de compras
historial_compras = HistorialCompras('Commons/historial_compras.json')



def abrir_historial_compras():
    historial_compras.mostrar_historial()
