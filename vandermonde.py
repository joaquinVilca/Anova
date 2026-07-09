# vandermonde.py
# Construye la matriz de diseño para regresion polinomial de grado k.
# Genera SOLO las columnas x^1, x^2, ..., x^k (sin columna de unos).
# modelo.py agrega la columna de intercepto cuando con_intercepto=True.
#
# Teoria: el modelo Y = b0 + b1*x + b2*x^2 + ... + bk*x^k
# en forma matricial es Y = X*beta con X la matriz de Vandermonde
# (incluyendo la columna de 1s que agrega modelo.py).

def construir(x, grado):
    # Valida que haya suficientes datos para estimar.
    # Con intercepto el modelo tiene grado+1 parametros,
    # se necesitan al menos grado+2 observaciones para gl_err >= 1.
    n = len(x)
    if n < grado + 2:
        print("AVISO: necesitas al menos")
        print(str(grado + 2) + " datos para grado " + str(grado))
    X = []
    for xi in x:
        fila = []
        for p in range(1, grado + 1):
            fila.append(float(xi) ** p)
        X.append(fila)
    return X

def etiquetas_pol(grado):
    # Genera las etiquetas legibles de cada coeficiente:
    # b0 (intercepto), x, x^2, x^3, ..., x^k
    et = ["b0", "x"]
    for p in range(2, grado + 1):
        et.append("x^" + str(p))
    return et
