import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import tkinter as tk
from Pantallas.main_interface import InterfazClasificacion

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazClasificacion(root)
    root.mainloop()