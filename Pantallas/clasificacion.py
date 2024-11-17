import tkinter as tk
from tkinter import messagebox, scrolledtext
import serial
import os
import json

def abrir_clasificacion(parent):
    parent.withdraw()

    ventana_clasificacion = tk.Toplevel()
    ventana_clasificacion.title("Clasificador - Interfaz Arduino")
    ventana_clasificacion.geometry("800x600")
    ventana_clasificacion.configure(bg="#FCC509")

    label = tk.Label(ventana_clasificacion, text="Clasificador - Conexión Arduino", font=("Arial", 22), bg="#FCC509", fg="black")
    label.pack(pady=10)

    salida_texto = scrolledtext.ScrolledText(ventana_clasificacion, wrap=tk.WORD, width=80, height=20, font=("Arial", 12))
    salida_texto.pack(pady=20)

    ruta_inventario = os.path.join("Commons", "inventario.json")

    puerto_serial = "COM3"  # Cambia esto al puerto donde está conectado tu Arduino
    velocidad_baudios = 9600

    try:
        arduino = serial.Serial(puerto_serial, velocidad_baudios, timeout=2)
        messagebox.showinfo("Conexión Exitosa", f"Conectado a Arduino en {puerto_serial}")
        arduino.write("APAGAR\n".encode('utf-8'))
    except serial.SerialException as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {puerto_serial}.\nError: {e}")
        ventana_clasificacion.destroy()
        parent.deiconify()
        return

    clasificacion_en_proceso = [False]

    def procesar_clasificacion():
        if clasificacion_en_proceso[0]:
            messagebox.showwarning("Clasificación en Proceso", "Primero termine la clasificación actual.")
            return

        try:
            arduino.flushInput()
            arduino.write("CLASIFICAR\n".encode('utf-8'))

            linea = arduino.readline().decode('utf-8').strip()
            if linea:
                salida_texto.insert(tk.END, f"Arduino: {linea}\n")
                salida_texto.see(tk.END)
                codigo_detectado = extraer_codigo(linea)

                if codigo_detectado:
                    actualizar_inventario(codigo_detectado)
                    if "PAP-001" in linea:
                        arduino.write("PARPADEAR:BLANCO\n".encode('utf-8'))
                    elif "TOM-003" in linea:
                        arduino.write("PARPADEAR:AZUL\n".encode('utf-8'))
                    elif "TOM-002" in linea:
                        arduino.write("PARPADEAR:VERDE\n".encode('utf-8'))
                    elif "MAL-001" in linea:
                        arduino.write("PARPADEAR:ROJO\n".encode('utf-8'))
                    clasificacion_en_proceso[0] = True
                else:
                    salida_texto.insert(tk.END, "No se detectó un código válido.\n")
                    salida_texto.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def terminar_clasificacion():
        if not clasificacion_en_proceso[0]:
            messagebox.showwarning("Sin Clasificación", "No hay una clasificación activa.")
            return

        try:
            arduino.write("TERMINAR\n".encode('utf-8'))
            clasificacion_en_proceso[0] = False
            salida_texto.insert(tk.END, "Clasificación finalizada.\n")
            salida_texto.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo terminar la clasificación: {e}")

    def extraer_codigo(linea):
        if "(" in linea and ")" in linea:
            inicio = linea.index("(") + 1
            fin = linea.index(")")
            return linea[inicio:fin].strip()
        return None

    def actualizar_inventario(codigo_detectado):
        try:
            with open(ruta_inventario, "r") as inv_file:
                inventario = json.load(inv_file)

            if codigo_detectado in inventario:
                inventario[codigo_detectado] += 1
                salida_texto.insert(tk.END, f"Inventario actualizado: +1 a {codigo_detectado}\n")
                salida_texto.see(tk.END)
            else:
                salida_texto.insert(tk.END, f"Código {codigo_detectado} no encontrado en el inventario.\n")
                salida_texto.see(tk.END)

            with open(ruta_inventario, "w") as inv_file:
                json.dump(inventario, inv_file)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            salida_texto.insert(tk.END, f"Error al actualizar el inventario: {e}\n")
            salida_texto.see(tk.END)

    boton_comenzar = tk.Button(ventana_clasificacion, text="Comenzar Clasificación", command=procesar_clasificacion,
                               bg="green", fg="white", width=20, height=2)
    boton_comenzar.pack(pady=10)

    boton_terminar = tk.Button(ventana_clasificacion, text="Terminar Clasificación", command=terminar_clasificacion,
                                bg="red", fg="white", width=20, height=2)
    boton_terminar.pack(pady=10)

    def regresar():
        try:
            arduino.write("APAGAR\n".encode('utf-8'))
            arduino.close()
        except Exception as e:
            salida_texto.insert(tk.END, f"Error al cerrar conexión con Arduino: {e}\n")
        ventana_clasificacion.destroy()
        parent.deiconify()

    boton_volver = tk.Button(ventana_clasificacion, text="Volver", command=regresar, bg="white", fg="#B90518", width=20, height=2)
    boton_volver.pack(pady=10)
