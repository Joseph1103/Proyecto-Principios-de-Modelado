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

    # Botón para abrir la ventana de Clasificador
    boton_clasificador = tk.Button(clasificador_ventana, text="Clasificador", command=lambda: abrir_ventana_clasificador(clasificador_ventana, root),
                                   bg="white", fg="#B90518", width=25, height=2)
    boton_clasificador.pack(pady=10)

    # Botón para abrir la ventana de BOM
    boton_bom = tk.Button(clasificador_ventana, text="BOM", command=lambda: abrir_ventana_bom(clasificador_ventana, root),
                          bg="white", fg="#B90518", width=25, height=2)
    boton_bom.pack(pady=10)

    # Botón para cerrar la ventana del clasificador y volver a la ventana principal
    boton_cerrar = tk.Button(clasificador_ventana, text="Cerrar Clasificador", command=lambda: cerrar_clasificador(root, clasificador_ventana),
                             bg="white", fg="#B90518", width=25, height=2)
    boton_cerrar.pack(pady=20)

def abrir_ventana_clasificador(parent, root):
    # Cierra la ventana principal del clasificador
    parent.withdraw()

    # Crear una nueva ventana para la funcionalidad de Clasificador
    ventana_clasificador = tk.Toplevel(root)
    ventana_clasificador.title("Ventana Clasificador")
    ventana_clasificador.geometry("800x600")
    ventana_clasificador.configure(bg="#FCC509")

    # Etiqueta de título
    label = tk.Label(ventana_clasificador, text="Ventana Clasificador", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=50)

    # Botón para volver a la ventana del clasificador
    boton_volver = tk.Button(ventana_clasificador, text="Volver", command=lambda: regresar_al_clasificador(ventana_clasificador, parent),
                             bg="white", fg="#B90518", width=25, height=2)
    boton_volver.pack(pady=20)

def abrir_ventana_bom(parent, root):
    # Cierra la ventana principal del clasificador
    parent.withdraw()

    # Crear una nueva ventana para la funcionalidad de BOM
    ventana_bom = tk.Toplevel(root)
    ventana_bom.title("Ventana BOM")
    ventana_bom.geometry("800x600")
    ventana_bom.configure(bg="#FCC509")

    # Etiqueta de título
    label = tk.Label(ventana_bom, text="Ventana BOM", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=50)

    # Botón para volver a la ventana del clasificador
    boton_volver = tk.Button(ventana_bom, text="Volver", command=lambda: regresar_al_clasificador(ventana_bom, parent),
                             bg="white", fg="#B90518", width=25, height=2)
    boton_volver.pack(pady=20)

def regresar_al_clasificador(ventana_actual, clasificador_ventana):
    ventana_actual.destroy()  # Cierra la ventana actual (BOM o Clasificador)
    clasificador_ventana.deiconify()  # Vuelve a mostrar la ventana principal del clasificador

def cerrar_clasificador(root, clasificador_ventana):
    clasificador_ventana.destroy()  # Cierra la ventana del clasificador
    root.deiconify()  # Muestra de nuevo la ventana principal
