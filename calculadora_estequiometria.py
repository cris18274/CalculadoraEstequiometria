import tkinter as tk
from tkinter import messagebox
from chemparse import parse_formula
from sympy import symbols, Eq, solve

def balancear_ecuacion():
    reactantes = entrada_reactantes.get().strip()
    productos = entrada_productos.get().strip()

    if not reactantes or not productos:
        messagebox.showerror("Error", "Por favor ingresa reactantes y productos.")
        return

    try:
        reactantes_dict = parse_formula(reactantes)
        productos_dict = parse_formula(productos)
    except Exception as e:
        messagebox.showerror("Error", f"Error al analizar la fórmula: {e}")
        return

    elementos = set(reactantes_dict.keys()) | set(productos_dict.keys())
    ecuaciones = []
    for elemento in elementos:
        reactante_coef = reactantes_dict.get(elemento, 0)
        producto_coef = productos_dict.get(elemento, 0)
        ecuaciones.append(Eq(reactante_coef, producto_coef))

    solucion = solve(ecuaciones, dict=True)

    resultado = ""
    for elemento in elementos:
        resultado += f"{elemento}{solucion[0][elemento] if solucion else ''} "

    resultado_balanceado.set(resultado.strip())

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Estequiometría")

# Etiqueta y entrada para los reactantes
tk.Label(ventana, text="Reactantes:").grid(row=0, column=0)
entrada_reactantes = tk.Entry(ventana)
entrada_reactantes.grid(row=0, column=1)

# Etiqueta y entrada para los productos
tk.Label(ventana, text="Productos:").grid(row=1, column=0)
entrada_productos = tk.Entry(ventana)
entrada_productos.grid(row=1, column=1)

# Botón para balancear la ecuación
boton_balancear = tk.Button(ventana, text="Balancear", command=balancear_ecuacion)
boton_balancear.grid(row=2, columnspan=2)

# Etiqueta para mostrar el resultado balanceado
resultado_balanceado = tk.StringVar()
tk.Label(ventana, text="Resultado:").grid(row=3, column=0)
tk.Label(ventana, textvariable=resultado_balanceado).grid(row=3, column=1)

ventana.mainloop()
