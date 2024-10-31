import tkinter as tk

def abrir_clasificador(root):
    # Crear una nueva ventana del clasificador
    clasificador_ventana = tk.Toplevel(root)
    clasificador_ventana.title("Clasificador")
    clasificador_ventana.geometry("800x600")
    clasificador_ventana.configure(bg="#FCC509")

    # Título de la ventana del clasificador
    label_clasificador = tk.Label(clasificador_ventana, text="Bienvenido al Clasificador", font=("Arial", 22), bg="#FCC509", fg="black")
    label_clasificador.pack(pady=50)

    # Aquí puedes agregar más widgets específicos para la funcionalidad del clasificador

    # Botón para cerrar la ventana del clasificador y volver a la ventana principal
    boton_cerrar = tk.Button(clasificador_ventana, text="Cerrar Clasificador", command=lambda: cerrar_clasificador(root, clasificador_ventana),
                             bg="white", fg="#B90518", width=25, height=2)
    boton_cerrar.pack(pady=20)

def cerrar_clasificador(root, clasificador_ventana):
    clasificador_ventana.destroy()  # Cierra la ventana del clasificador
    root.deiconify()  # Muestra de nuevo la ventana principal
