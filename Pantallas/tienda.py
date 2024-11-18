import tkinter as tk
from tkinter import ttk
from Pantallas.carrito import abrir_carrito
from tkinter import font
from tkinter import messagebox
from Pantallas.Historial_comp import abrir_historial_compras

def cargar_productos(nombre_archivo):
    productos = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            nombre, precio, cantidad = linea.strip().split(',')
            productos.append({
                'nombre': nombre,
                'precio': float(precio),
                'cantidad': int(cantidad)
            })
    return productos

def agregar_al_carrito(nombre, precio, carrito, productos):
    # Verifica si el producto ya está en el carrito y actualiza la cantidad
    for item in carrito:
        if item['nombre'] == nombre:
            # Busca el producto en el inventario para verificar la cantidad disponible
            producto_en_inventario = next((p for p in productos if p['nombre'] == nombre), None)
            if producto_en_inventario:
                if item['cantidad'] < producto_en_inventario['cantidad']:
                    item['cantidad'] += 1  # Si hay stock disponible, agrega uno más al carrito
                else:
                    # Mostrar mensaje emergente si no hay más stock disponible
                    messagebox.showinfo("Sin stock", f"No se puede agregar más {nombre}, solo hay {producto_en_inventario['cantidad']} disponibles.")
            return

    # Si no está en el carrito, lo agrega con cantidad 1
    producto_en_inventario = next((p for p in productos if p['nombre'] == nombre), None)
    if producto_en_inventario:
        if 1 <= producto_en_inventario['cantidad']:
            carrito.append({'nombre': nombre, 'precio': precio, 'cantidad': 1})
        else:
            # Mostrar mensaje emergente si no hay stock disponible
            messagebox.showinfo("Sin stock", f"No se puede agregar {nombre}, no hay stock disponible.")

def abrir_tienda(root):
    # Crear una nueva ventana de la tienda
    tienda_ventana = tk.Toplevel(root)
    tienda_ventana.title("Tienda")
    tienda_ventana.geometry("800x800")
    tienda_ventana.configure(bg="#FCC509")

    # Título de la ventana de la tienda
    label_tienda = tk.Label(tienda_ventana, text="Bienvenido a la Tienda", font=("Arial", 22), bg="#FCC509", fg="black")
    label_tienda.place(x=250, y=20)

    # Frame para el Treeview y las entradas
    frame_tree = tk.Frame(tienda_ventana, bg="#FCC509")
    frame_tree.place(x=150, y=70, width=900, height=550)

    # Aquí puedes agregar más widgets específicos para la funcionalidad de la tienda

    productos = cargar_productos('Commons/articulos.txt')

    # Define el estilo para el Treeview y ajusta la altura de las filas
    style = ttk.Style()
    style.configure("Treeview", rowheight=30)  # Ajusta el valor de rowheight según la altura deseada

    # Configuración del Treeview
    tree = ttk.Treeview(frame_tree, columns=('Nombre', 'Precio', 'Cantidad', 'Comprar'), show='headings', height=10)
    tree.heading('Nombre', text='Nombre', anchor='center')
    tree.heading('Precio', text='Precio', anchor='center')
    tree.heading('Cantidad', text='Cantidad', anchor='center')
    tree.heading('Comprar', text='Comprar', anchor='center')

    tree.column('Nombre', width=300)
    tree.column('Precio', width=100)
    tree.column('Cantidad', width=100)
    tree.column('Comprar', width=100)

    tree.pack(side='left', fill='y')

    # Configuración de la barra de desplazamiento
    scrollbar = ttk.Scrollbar(frame_tree, orient='vertical', command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    carrito = []

    fuente_personalizada = font.Font(size=8)

    for producto in productos:
        # Insertar cada producto en el Treeview
        tree.insert('', 'end', values=(producto['nombre'], producto['precio'], producto['cantidad']))

        # Crear un botón para agregar al carrito
        boton_agregar = tk.Button(tienda_ventana, text="Agregar",
        command=lambda nombre=producto['nombre'],precio=producto['precio']: agregar_al_carrito(nombre, precio, carrito,
        productos), bg="white", fg="#B90518", width=6,font=fuente_personalizada, padx=5, pady=0)
        boton_agregar.place(x=680, y=100 + 30 * productos.index(producto))

    boton_carrito = tk.Button(tienda_ventana, text="Ver Carrito", command=lambda: abrir_carrito(carrito, productos),
    bg="white", fg="#B90518", width=20)
    boton_carrito.place(x=350, y=700)

    boton_historial = tk.Button(tienda_ventana, text="Historial de Compras", command=lambda: abrir_historial_compras(),
    bg="white", fg="#B90518", width=20)
    boton_historial.place(x=350, y=660)

    # Botón para cerrar la tienda y volver a la ventana principal
    boton_cerrar = tk.Button(tienda_ventana, text="Cerrar Tienda", command=lambda: cerrar_tienda(root, tienda_ventana),
    bg="white", fg="#B90518", width=25, height=2)
    boton_cerrar.place(x=325, y=740)

def cerrar_tienda(root, tienda_ventana):
    tienda_ventana.destroy()  # Cierra la ventana de la tienda
    root.deiconify()
