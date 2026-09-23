import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# VARIABLES GLOBALES
# ============================================================

q_objetivo_global = 0
cuotas_global = 0
tolerancia_global = 0


# ============================================================
# CÁLCULO PARA 2 PRODUCTOS
# ============================================================

def calcular_2_productos(c1, max_r1, c2, max_r2, S_objetivo, tolerancia):

    mejor_resultado = None
    menor_diferencia = float("inf")

    for r1 in range(max_r1, -1, -1):

        capital1 = c1 * (1 - r1 / 100)

        capital2_necesario = S_objetivo - capital1

        r2 = round(
            (1 - capital2_necesario / c2) * 100
        )

        if 0 <= r2 <= max_r2:

            capital2 = c2 * (1 - r2 / 100)

            S_obtenido = capital1 + capital2

            q_obtenida = S_obtenido / cuotas_global

            diferencia = abs(
                q_obtenida - q_objetivo_global
            )

            if diferencia < menor_diferencia:

                menor_diferencia = diferencia

                mejor_resultado = {
                    "r1": r1,
                    "r2": r2,
                    "r3": None,
                    "S_obtenido": S_obtenido,
                    "q_obtenida": q_obtenida,
                    "diferencia": diferencia
                }

            if diferencia <= tolerancia:
                return mejor_resultado, True

    return mejor_resultado, False


# ============================================================
# CÁLCULO PARA 3 PRODUCTOS
# ============================================================

def calcular_3_productos(
    c1, max_r1,
    c2, max_r2,
    c3, max_r3,
    S_objetivo,
    tolerancia
):

    mejor_resultado = None
    menor_diferencia = float("inf")

    for r1 in range(max_r1, -1, -1):

        capital1 = c1 * (1 - r1 / 100)

        for r2 in range(max_r2, -1, -1):

            capital2 = c2 * (1 - r2 / 100)

            capital3_necesario = (
                S_objetivo
                - capital1
                - capital2
            )

            r3 = round(
                (1 - capital3_necesario / c3) * 100
            )

            if 0 <= r3 <= max_r3:

                capital3 = c3 * (1 - r3 / 100)

                S_obtenido = (
                    capital1
                    + capital2
                    + capital3
                )

                q_obtenida = S_obtenido / cuotas_global

                diferencia = abs(
                    q_obtenida - q_objetivo_global
                )

                if diferencia < menor_diferencia:

                    menor_diferencia = diferencia

                    mejor_resultado = {
                        "r1": r1,
                        "r2": r2,
                        "r3": r3,
                        "S_obtenido": S_obtenido,
                        "q_obtenida": q_obtenida,
                        "diferencia": diferencia
                    }

                if diferencia <= tolerancia:
                    return mejor_resultado, True

    return mejor_resultado, False


# ============================================================
# CONVERSIÓN DE NÚMEROS
# ============================================================

def obtener_numero(campo):

    texto = campo.get().strip()

    if texto == "":
        raise ValueError("Hay un campo vacío.")

    texto = texto.replace(".", "").replace(",", ".")

    return float(texto)


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

def mostrar_resultado(resultado, encontrado):

    if resultado is None:

        txt_resultado.delete("1.0", tk.END)

        txt_resultado.insert(
            tk.END,
            "NO SE ENCONTRÓ UNA SOLUCIÓN DENTRO DE LOS RANGOS.\n"
        )

        return

    r1 = resultado["r1"]
    r2 = resultado["r2"]
    r3 = resultado["r3"]

    S_obtenido = resultado["S_obtenido"]
    q_obtenida = resultado["q_obtenida"]
    diferencia = resultado["diferencia"]

    S_objetivo = q_objetivo_global * cuotas_global

    txt_resultado.delete("1.0", tk.END)

    # ========================================================
    # REBAJAS PRIMERO
    # ========================================================

    txt_resultado.insert(
        tk.END,
        "REBAJAS\n"
    )

    txt_resultado.insert(
        tk.END,
        "======================================\n\n"
    )

    txt_resultado.insert(
        tk.END,
        f"r1 = {r1}%\n"
    )

    txt_resultado.insert(
        tk.END,
        f"r2 = {r2}%\n"
    )

    if r3 is not None:

        txt_resultado.insert(
            tk.END,
            f"r3 = {r3}%\n"
        )

    # ========================================================
    # COMPROBACIÓN
    # ========================================================

    txt_resultado.insert(
        tk.END,
        "\n--------------------------------------\n"
    )

    txt_resultado.insert(
        tk.END,
        "COMPROBACIÓN\n"
    )

    txt_resultado.insert(
        tk.END,
        "--------------------------------------\n\n"
    )

    txt_resultado.insert(
        tk.END,
        f"Cuotas : {cuotas_global}\n"
    )

    txt_resultado.insert(
        tk.END,
        f"Cuota objetivo : ${q_objetivo_global:,.2f}\n"
    )

    txt_resultado.insert(
        tk.END,
        f"Cuota obtenida : ${q_obtenida:,.2f}\n"
    )

    txt_resultado.insert(
        tk.END,
        f"Diferencia de cuota : ${diferencia:,.2f}\n\n"
    )

    txt_resultado.insert(
        tk.END,
        f"S objetivo : ${S_objetivo:,.2f}\n"
    )

    txt_resultado.insert(
        tk.END,
        f"S obtenido : ${S_obtenido:,.2f}\n"
    )

    # ========================================================
    # ESTADO
    # ========================================================

    txt_resultado.insert(
        tk.END,
        "\n--------------------------------------\n"
    )

    if encontrado:

        txt_resultado.insert(
            tk.END,
            "✓ SOLUCIÓN ENCONTRADA\n"
        )

        txt_resultado.insert(
            tk.END,
            "--------------------------------------\n"
        )

        txt_resultado.insert(
            tk.END,
            f"La diferencia está dentro de la "
            f"tolerancia de ${tolerancia_global:,.2f}.\n"
        )

    else:

        txt_resultado.insert(
            tk.END,
            "⚠ SOLUCIÓN MÁS CERCANA\n"
        )

        txt_resultado.insert(
            tk.END,
            "--------------------------------------\n"
        )

        txt_resultado.insert(
            tk.END,
            f"No se encontró una combinación dentro "
            f"de la tolerancia de ${tolerancia_global:,.2f}.\n"
        )

        txt_resultado.insert(
            tk.END,
            "Se muestra la combinación más cercana encontrada.\n"
        )


# ============================================================
# MOSTRAR / OCULTAR PRODUCTO 3
# ============================================================

def actualizar_productos(event=None):

    cantidad = combo_productos.get()

    if cantidad == "3":

        frame_producto3.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

    else:

        frame_producto3.grid_remove()

    actualizar_scroll()


# ============================================================
# ACTUALIZAR ÁREA DE SCROLL
# ============================================================

def actualizar_scroll(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


# ============================================================
# FUNCIÓN PRINCIPAL DE CÁLCULO
# ============================================================

def calcular():

    global q_objetivo_global
    global cuotas_global
    global tolerancia_global

    try:

        # ----------------------------------------------------
        # DATOS GENERALES
        # ----------------------------------------------------

        cuotas = int(
            entrada_cuotas.get().strip()
        )

        if cuotas <= 0:
            raise ValueError(
                "La cantidad de cuotas debe ser mayor que 0."
            )

        q_objetivo = obtener_numero(
            entrada_cuota
        )

        tolerancia = obtener_numero(
            entrada_tolerancia
        )

        if q_objetivo <= 0:
            raise ValueError(
                "La cuota objetivo debe ser mayor que 0."
            )

        if tolerancia < 0:
            raise ValueError(
                "La tolerancia no puede ser negativa."
            )

        # ----------------------------------------------------
        # PRODUCTO 1
        # ----------------------------------------------------

        c1 = obtener_numero(
            entrada_c1
        )

        max_r1 = int(
            obtener_numero(
                entrada_r1
            )
        )

        # ----------------------------------------------------
        # PRODUCTO 2
        # ----------------------------------------------------

        c2 = obtener_numero(
            entrada_c2
        )

        max_r2 = int(
            obtener_numero(
                entrada_r2
            )
        )

        if c1 <= 0 or c2 <= 0:
            raise ValueError(
                "Los capitales deben ser mayores que 0."
            )

        if not 0 <= max_r1 <= 100:
            raise ValueError(
                "La rebaja máxima 1 debe estar entre 0% y 100%."
            )

        if not 0 <= max_r2 <= 100:
            raise ValueError(
                "La rebaja máxima 2 debe estar entre 0% y 100%."
            )

        # ----------------------------------------------------
        # DATOS GLOBALES
        # ----------------------------------------------------

        cuotas_global = cuotas
        q_objetivo_global = q_objetivo
        tolerancia_global = tolerancia

        S_objetivo = q_objetivo * cuotas

        # ----------------------------------------------------
        # 2 PRODUCTOS
        # ----------------------------------------------------

        if combo_productos.get() == "2":

            resultado, encontrado = calcular_2_productos(
                c1,
                max_r1,
                c2,
                max_r2,
                S_objetivo,
                tolerancia
            )

        # ----------------------------------------------------
        # 3 PRODUCTOS
        # ----------------------------------------------------

        else:

            c3 = obtener_numero(
                entrada_c3
            )

            max_r3 = int(
                obtener_numero(
                    entrada_r3
                )
            )

            if c3 <= 0:
                raise ValueError(
                    "El capital 3 debe ser mayor que 0."
                )

            if not 0 <= max_r3 <= 100:
                raise ValueError(
                    "La rebaja máxima 3 debe estar entre 0% y 100%."
                )

            resultado, encontrado = calcular_3_productos(
                c1,
                max_r1,
                c2,
                max_r2,
                c3,
                max_r3,
                S_objetivo,
                tolerancia
            )

        # ----------------------------------------------------
        # MOSTRAR RESULTADO
        # ----------------------------------------------------

        mostrar_resultado(
            resultado,
            encontrado
        )

        actualizar_scroll()

    except ValueError as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

    except Exception as e:

        messagebox.showerror(
            "Error inesperado",
            f"Ocurrió un error:\n\n{e}"
        )


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

ventana = tk.Tk()

ventana.title(
    "Calculadora de Rebajas"
)

ventana.geometry(
    "700x750"
)

ventana.resizable(
    True,
    True
)

ventana.minsize(
    550,
    500
)


# ============================================================
# CONTENEDOR PRINCIPAL CON SCROLL
# ============================================================

contenedor_canvas = tk.Frame(
    ventana
)

contenedor_canvas.pack(
    fill="both",
    expand=True
)


# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(
    contenedor_canvas,
    highlightthickness=0
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# SCROLLBAR VERTICAL
# ============================================================

scrollbar = ttk.Scrollbar(
    contenedor_canvas,
    orient="vertical",
    command=canvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)


# ============================================================
# FRAME DENTRO DEL CANVAS
# ============================================================

contenido = tk.Frame(
    canvas
)

ventana_canvas = canvas.create_window(
    (0, 0),
    window=contenido,
    anchor="nw"
)


# ============================================================
# AJUSTAR ANCHO
# ============================================================

def ajustar_ancho(event):

    canvas.itemconfig(
        ventana_canvas,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    ajustar_ancho
)

contenido.bind(
    "<Configure>",
    actualizar_scroll
)


# ============================================================
# RUEDA DEL MOUSE
# ============================================================

def scroll_mouse(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    scroll_mouse
)


# ============================================================
# TÍTULO
# ============================================================

titulo = tk.Label(
    contenido,
    text="CALCULADORA DE REBAJAS",
    font=("Arial", 18, "bold")
)

titulo.grid(
    row=0,
    column=0,
    columnspan=2,
    pady=(15, 15)
)


# ============================================================
# DATOS GENERALES
# ============================================================

frame_general = ttk.LabelFrame(
    contenido,
    text="Datos generales"
)

frame_general.grid(
    row=1,
    column=0,
    columnspan=2,
    padx=15,
    pady=5,
    sticky="ew"
)


# Cantidad de productos

tk.Label(
    frame_general,
    text="Cantidad de productos:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

combo_productos = ttk.Combobox(
    frame_general,
    values=["2", "3"],
    state="readonly",
    width=10
)

combo_productos.set("3")

combo_productos.grid(
    row=0,
    column=1,
    padx=10,
    pady=7
)

combo_productos.bind(
    "<<ComboboxSelected>>",
    actualizar_productos
)


# Cantidad de cuotas

tk.Label(
    frame_general,
    text="Cantidad de cuotas:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_cuotas = tk.Entry(
    frame_general,
    width=15
)

entrada_cuotas.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# Cuota objetivo

tk.Label(
    frame_general,
    text="Valor cuota objetivo:"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_cuota = tk.Entry(
    frame_general,
    width=15
)

entrada_cuota.grid(
    row=2,
    column=1,
    padx=10,
    pady=7
)


# Tolerancia

tk.Label(
    frame_general,
    text="Tolerancia:"
).grid(
    row=3,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_tolerancia = tk.Entry(
    frame_general,
    width=15
)

# POR DEFECTO: 0
entrada_tolerancia.insert(
    0,
    "0"
)

entrada_tolerancia.grid(
    row=3,
    column=1,
    padx=10,
    pady=7
)


# Paso fijo

tk.Label(
    frame_general,
    text="Paso de rebaja:"
).grid(
    row=4,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

tk.Label(
    frame_general,
    text="1% (fijo)"
).grid(
    row=4,
    column=1,
    padx=10,
    pady=7
)


# ============================================================
# PRODUCTOS
# ============================================================

frame_productos = ttk.LabelFrame(
    contenido,
    text="Productos"
)

frame_productos.grid(
    row=2,
    column=0,
    columnspan=2,
    padx=15,
    pady=10,
    sticky="ew"
)

frame_productos.columnconfigure(
    0,
    weight=1
)


# ============================================================
# PRODUCTO 1
# ============================================================

frame_producto1 = ttk.LabelFrame(
    frame_productos,
    text="Producto 1"
)

frame_producto1.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="ew"
)

tk.Label(
    frame_producto1,
    text="Capital 1:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_c1 = tk.Entry(
    frame_producto1,
    width=15
)

entrada_c1.grid(
    row=0,
    column=1,
    padx=10,
    pady=7
)


tk.Label(
    frame_producto1,
    text="Rebaja máxima 1:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_r1 = tk.Entry(
    frame_producto1,
    width=15
)

entrada_r1.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# ============================================================
# PRODUCTO 2
# ============================================================

frame_producto2 = ttk.LabelFrame(
    frame_productos,
    text="Producto 2"
)

frame_producto2.grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="ew"
)

tk.Label(
    frame_producto2,
    text="Capital 2:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_c2 = tk.Entry(
    frame_producto2,
    width=15
)

entrada_c2.grid(
    row=0,
    column=1,
    padx=10,
    pady=7
)


tk.Label(
    frame_producto2,
    text="Rebaja máxima 2:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_r2 = tk.Entry(
    frame_producto2,
    width=15
)

entrada_r2.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# ============================================================
# PRODUCTO 3
# ============================================================

frame_producto3 = ttk.LabelFrame(
    frame_productos,
    text="Producto 3"
)

frame_producto3.grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="ew"
)

tk.Label(
    frame_producto3,
    text="Capital 3:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_c3 = tk.Entry(
    frame_producto3,
    width=15
)

entrada_c3.grid(
    row=0,
    column=1,
    padx=10,
    pady=7
)


tk.Label(
    frame_producto3,
    text="Rebaja máxima 3:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=7,
    sticky="w"
)

entrada_r3 = tk.Entry(
    frame_producto3,
    width=15
)

entrada_r3.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# ============================================================
# BOTÓN CALCULAR
# ============================================================

boton_calcular = tk.Button(
    contenido,
    text="CALCULAR",
    command=calcular,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8
)

boton_calcular.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10
)


# ============================================================
# RESULTADO
# ============================================================

frame_resultado = ttk.LabelFrame(
    contenido,
    text="Resultado"
)

frame_resultado.grid(
    row=4,
    column=0,
    columnspan=2,
    padx=15,
    pady=(5, 20),
    sticky="ew"
)

frame_resultado.columnconfigure(
    0,
    weight=1
)

frame_resultado.rowconfigure(
    0,
    weight=1
)


txt_resultado = tk.Text(
    frame_resultado,
    width=70,
    height=16,
    font=("Consolas", 11),
    wrap="word"
)

txt_resultado.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="ew"
)


# ============================================================
# SCROLLBAR DEL RESULTADO
# ============================================================

scroll_resultado = ttk.Scrollbar(
    frame_resultado,
    orient="vertical",
    command=txt_resultado.yview
)

scroll_resultado.grid(
    row=0,
    column=1,
    pady=10,
    sticky="ns"
)

txt_resultado.configure(
    yscrollcommand=scroll_resultado.set
)


# ============================================================
# INICIAR
# ============================================================

actualizar_scroll()

ventana.mainloop()