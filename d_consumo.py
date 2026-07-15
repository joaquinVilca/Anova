# datos_consumo.py
# Cantidad consumida (Y), precio del articulo (X1), ingreso (X2)
# y precio del sustituto (X3). Periodo 1970-1984.

ANIO = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]

Y  = [40, 45, 50, 55, 60, 70, 65, 65, 75, 75, 80, 100, 90, 95, 85]
X1 = [9, 8, 9, 8, 7, 6, 6, 8, 5, 5, 5, 3, 4, 3, 4]
X2 = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
X3 = [10, 14, 12, 13, 11, 15, 16, 17, 22, 19, 20, 23, 18, 24, 21]
X4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# Lista con todas las variables X disponibles
TODAS_LAS_X = [X1, X2, X3, X4]

def matriz_X():
    # X = [X1, X2, X3...] (SIN columna de 1's)
    try:
        k = int(input("¿Cuantos X quieres ingresar?: "))
    except ValueError:
        k = len(TODAS_LAS_X) # por defecto todas
    
    n = len(Y)
    X = []
    # Nos aseguramos de no pedir mas de lo que hay
    k = min(k, len(TODAS_LAS_X))
    
    for i in range(n):
        fila = []
        for j in range(k):
            fila.append(float(TODAS_LAS_X[j][i]))
        X.append(fila)
    return X, k


def vector_Y():
    return [float(v) for v in Y]
