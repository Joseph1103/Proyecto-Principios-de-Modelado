import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
from Pantallas.tienda import abrir_tienda  # Importamos la función de tienda.py
from Pantallas.clasificador import abrir_clasificador  # Importamos la función de clasificador.py

class InterfazClasificacion:
    def __init__(self, root):
        self.root = root
        self.crear_ventana_principal()

    def crear_ventana_principal(self):
        self.root.title("Sistema de Clasificación de Productos")
        self.root.geometry("800x600")
        self.root.configure(bg="#FCC509")

        # Limpiar widgets antiguos si existen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(self.root, text="Corporación de agricultores unidos",
                               font=("Arial", 22), bg="#FCC509", fg="black")
        title_label.place(x=160, y=50)

        # Botón Cliente para abrir ventana
        boton_1 = tk.Button(self.root, text="Cliente", command=self.abrir_ventana_cliente, bg="white", fg="#B90518",
                            width=25, height=2)
        boton_1.place(x=200, y=250)

        # Botón Operador para abrir ventana
        boton_2 = tk.Button(self.root, text="Operador", command=self.abrir_ventana_operador, bg="white", fg="#B90518",
                            width=25, height=2)
        boton_2.place(x=400, y=250)

    def abrir_ventana_cliente(self):
        # Limpiar widgets de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        # Configuración de la nueva ventana (Cliente)
        self.root.title("Ventana Cliente - Sistema de Clasificación")
        self.root.configure(bg="#FCC509")

        # Título de la nueva ventana
        title_label = tk.Label(self.root, text="Cliente",
                               font=("Arial", 22), bg="#FCC509", fg="black")
        title_label.place(x=350, y=50)

        # Campo de entrada para Usuario
        usuario_label = tk.Label(self.root, text="Usuario: ", font=("Arial", 14), bg="#FCC509", fg="black")
        usuario_label.place(x=200, y=150)
        self.usuario_entry = tk.Entry(self.root, font=("Arial", 14), width=20)
        self.usuario_entry.place(x=300, y=150)

        # Campo de entrada para Contraseña
        contrasena_label = tk.Label(self.root, text="Contraseña: ", font=("Arial", 14), bg="#FCC509", fg="black")
        contrasena_label.place(x=200, y=200)
        self.contrasena_entry = tk.Entry(self.root, font=("Arial", 14), width=20, show="*")
        self.contrasena_entry.place(x=300, y=200)

        # Botón para registrarse y guardar la información
        boton_registrarse = tk.Button(self.root, text="Registrarse", command=self.registrar_usuario_cliente, bg="white",
                                      fg="#B90518", width=25, height=2)
        boton_registrarse.place(x=300, y=250)

        # Botón para iniciar sesión
        boton_iniciar_sesion = tk.Button(self.root, text="Iniciar sesión", command=self.iniciar_sesion_cliente,
                                         bg="white", fg="#B90518", width=25, height=2)
        boton_iniciar_sesion.place(x=300, y=300)

        # Botón para entrar sin iniciar sesión
        boton_entrar_sin_sesion = tk.Button(self.root, text="Entrar sin iniciar sesión", command=self.entrar_sin_sesion,
                                            bg="white", fg="#B90518", width=25, height=2)
        boton_entrar_sin_sesion.place(x=300, y=350)

        # Botón para volver a la ventana principal
        boton_volver = tk.Button(self.root, text="Volver", command=self.crear_ventana_principal, bg="white", fg="#B90518",
                                 width=25, height=2)
        boton_volver.place(x=300, y=400)

    def abrir_ventana_operador(self):
        # Limpiar widgets de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        # Configuración de la nueva ventana (Operador)
        self.root.title("Ventana Operador - Sistema de Clasificación")
        self.root.configure(bg="#FCC509")

        # Título de la nueva ventana
        title_label = tk.Label(self.root, text="Operador",
                               font=("Arial", 22), bg="#FCC509", fg="black")
        title_label.place(x=350, y=50)

        # Campo de entrada para Usuario
        usuario_label = tk.Label(self.root, text="Usuario: ", font=("Arial", 14), bg="#FCC509", fg="black")
        usuario_label.place(x=200, y=150)
        self.usuario_entry = tk.Entry(self.root, font=("Arial", 14), width=20)
        self.usuario_entry.place(x=300, y=150)

        # Campo de entrada para Contraseña
        contrasena_label = tk.Label(self.root, text="Contraseña: ", font=("Arial", 14), bg="#FCC509", fg="black")
        contrasena_label.place(x=200, y=200)
        self.contrasena_entry = tk.Entry(self.root, font=("Arial", 14), width=20, show="*")
        self.contrasena_entry.place(x=300, y=200)

        # Botón para registrarse y guardar la información
        boton_registrarse = tk.Button(self.root, text="Registrarse", command=self.registrar_usuario_operador, bg="white",
                                      fg="#B90518", width=25, height=2)
        boton_registrarse.place(x=300, y=250)

        # Botón para iniciar sesión
        boton_iniciar_sesion = tk.Button(self.root, text="Iniciar sesión", command=self.iniciar_sesion_operador,
                                         bg="white", fg="#B90518", width=25, height=2)
        boton_iniciar_sesion.place(x=300, y=300)

        # Botón para volver a la ventana principal
        boton_volver = tk.Button(self.root, text="Volver", command=self.crear_ventana_principal, bg="white", fg="#B90518",
                                 width=25, height=2)
        boton_volver.place(x=300, y=350)

    def registrar_usuario_cliente(self):
        self.registrar_usuario("Commons/usuarios.txt")

    def registrar_usuario_operador(self):
        self.registrar_usuario("Commons/operadores.txt")

    def iniciar_sesion_cliente(self):
        self.iniciar_sesion("Commons/usuarios.txt", abrir_tienda, usuario_tipo="cliente", estado=0)

    def iniciar_sesion_operador(self):
        self.iniciar_sesion("Commons/operadores.txt", abrir_clasificador, usuario_tipo="operador", estado=0, guardar=False)

    def registrar_usuario(self, ruta_archivo):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        # Verifica que se haya ingresado usuario y contraseña
        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un usuario y una contraseña.")
            return

        # Crear la carpeta 'Commons' si no existe
        if not os.path.exists("Commons"):
            os.makedirs("Commons")

        # Guardar la información en el archivo
        with open(ruta_archivo, "a") as archivo:
            archivo.write(f"{usuario},{contrasena}\n")

        messagebox.showinfo("Registro", "Usuario registrado correctamente")

    def iniciar_sesion(self, ruta_archivo, funcion_abrir, usuario_tipo, estado, guardar=True):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if not os.path.exists(ruta_archivo):
            messagebox.showerror("Error", "No hay usuarios registrados.")
            return

        with open(ruta_archivo, "r") as archivo:
            for linea in archivo:
                usuario_registrado, contrasena_registrada = linea.strip().split(",")
                if usuario == usuario_registrado and contrasena == contrasena_registrada:
                    if guardar:
                        self.guardar_usuario_json(usuario)  # Guarda solo si `guardar=True`
                    self.root.withdraw()  # Oculta la ventana principal
                    funcion_abrir(self.root)
                    return


        # Mostrar mensaje de error si las credenciales no coinciden
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def entrar_sin_sesion(self):
        estado = 1  # Definir estado como 1 cuando entra sin usuario
        self.guardar_usuario_json("sin_usuario")  # Guardar en JSON solo con "sin_usuario"
        self.root.withdraw()
        abrir_tienda(self.root)

    def guardar_usuario_json(self, usuario):
        # Crea o actualiza un archivo JSON solo con el usuario
        datos = {"usuario": usuario}
        with open("Commons/usuario_sesion.json", "w") as archivo_json:
            json.dump(datos, archivo_json)

