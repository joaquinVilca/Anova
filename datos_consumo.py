# datos_consumo.py
# Cantidad consumida (Y), precio del articulo (X1), ingreso (X2)
# y precio del sustituto (X3). Periodo 1970-1984.

ANIO = [1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977,
        1978, 1979, 1980, 1981, 1982, 1983, 1984]

Y  = [40, 45, 50, 55, 60, 70, 65, 65, 75, 75, 80, 100, 90, 95, 85]
X1 = [9, 8, 9, 8, 7, 6, 6, 8, 5, 5, 5, 3, 4, 3, 4]
X2 = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
X3 = [10, 14, 12, 13, 11, 15, 16, 17, 22, 19, 20, 23, 18, 24, 21]


def matriz_X():
    # X = [X1, X2, X3]  (15x3), SIN columna de 1's.
    # modelo.construir_X() agrega el intercepto cuando con_intercepto=True.
    n = len(Y)
    X = []
    for i in range(n):
        X.append([float(X1[i]), float(X2[i]), float(X3[i])])
    return X


def vector_Y():
    return [float(v) for v in Y]
