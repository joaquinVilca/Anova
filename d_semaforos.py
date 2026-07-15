# datos_semaforos.py
# Datos del estudio de ingenieria de transito.
# Factor: tipo de semaforo (1=Programado, 2=Semiactivado, 3=Activado)
# Respuesta: retraso promedio (seg/vehiculo) en cada interseccion.

Y1 = [36.6, 39.2, 30.4 ]   # Programado
Y2 = [17.5, 20.6, 18.7,25.7]   # Semiactivado
Y3 = [15.0, 10.4, 18.9,15.2,10.5]   # Activado

GRUPOS = [Y1, Y2, Y3]
ETIQUETAS = ["Programado", "Semiactivado", "Activado"]


def vector_y():
    # Concatena los 3 grupos en un solo vector Y (orden: G1, G2, G3)
    y = []
    for g in GRUPOS:
        y = y + g
    return y


def n_por_grupo():
    return [len(g) for g in GRUPOS]


def matriz_indicadora():
    # Matriz X de INDICADORAS puras (modelo de celdas / medias, mu=0).
    # Columna k = 1 si la observacion pertenece al grupo k, 0 en otro caso.
    # X'X = diag(n1,n2,n3)  -> siempre invertible (rango completo = k grupos)
    k = len(GRUPOS)
    X = []
    for i in range(k):
        for _ in GRUPOS[i]:
            fila = [0.0] * k
            fila[i] = 1.0
            X.append(fila)
    return X


def matriz_dummies_referencia():
    # Matriz X SIN columna de 1's, solo dummies d2, d3 (grupo 1 = referencia).
    # modelo.construir_X() debe llamarse con con_intercepto=True para anadir
    # la columna de 1's -> Xm = [1, d2, d3], rango completo = 3.
    k = len(GRUPOS)
    X = []
    for i in range(k):
        for _ in GRUPOS[i]:
            fila = [0.0] * (k - 1)
            if i > 0:
                fila[i - 1] = 1.0
            X.append(fila)
    return X
