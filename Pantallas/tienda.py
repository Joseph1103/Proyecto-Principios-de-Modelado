import tkinter as tk

def abrir_tienda(root):
    # Crear una nueva ventana de la tienda
    tienda_ventana = tk.Toplevel(root)
    tienda_ventana.title("Tienda")
    tienda_ventana.geometry("800x600")
    tienda_ventana.configure(bg="#FCC509")

    # Título de la ventana de la tienda
    label_tienda = tk.Label(tienda_ventana, text="Bienvenido a la Tienda", font=("Arial", 22), bg="#FCC509", fg="black")
    label_tienda.pack(pady=50)

    # Aquí puedes agregar más widgets específicos para la funcionalidad de la tienda

    # Botón para cerrar la tienda y volver a la ventana principal
    boton_cerrar = tk.Button(tienda_ventana, text="Cerrar Tienda", command=lambda: cerrar_tienda(root, tienda_ventana),
                             bg="white", fg="#B90518", width=25, height=2)
    boton_cerrar.pack(pady=20)

def cerrar_tienda(root, tienda_ventana):
    tienda_ventana.destroy()  # Cierra la ventana de la tienda
    root.deiconify()  # Muestra de nuevo la ventana principal
